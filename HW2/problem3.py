#! /usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

from fuzzylogic.classes import Domain, Rule
from fuzzylogic.functions import R, S, triangular, singleton, bounded_sigmoid

from problem1 import get_histogram, plot_multi_histogram, bgr2grayscale

# ------------------------------------ DEO POD A ------------------------------------ 

def sigmoid(x: float, scale:float = 25., center:float = 125.) -> float:
    return 1/(1+math.exp(-(x-center)/scale))

def generate_lut(func: callable, begin: int = 0, end: int = 256) -> np.array:
    val_range = np.arange(begin, end)
    func_vect = np.vectorize(func)
    return func_vect(val_range).astype('float32')

def apply_custom_LUT(img: cv2.Mat, LUT) -> np.ndarray:
    return LUT[img]



# ------------------------------------ DEO POD B ------------------------------------

def fuzzy_contrast_enchancer(img: cv2.Mat, lvls_out: int = 511, new_black:int = 0, new_gray: int = 256, new_white:int = 511):

    in_domain = Domain('INPUT_VALUES', np.min(img), np.max(img))

    black = np.min(img)
    white = np.max(img)
    gray = (black + white) / 2

    # fuzzy antecedents
    in_domain.dark = bounded_sigmoid(black, gray, inverse=True)
    in_domain.light = bounded_sigmoid(gray, white)
    in_domain.medium = triangular(black, white)

    # fuzzy conclusions
    out_domain = Domain('OUTPUT_VALUE', 0, lvls_out)

    out_domain.dark = singleton(new_black)
    out_domain.medium = singleton(new_gray)
    out_domain.light = singleton(new_white)

    # Dummy rule because the library breaks without it
    in_dummy = Domain('Dummy domain for dummy library', 0, 2)
    in_dummy.dummy = singleton(1)

    R1 = Rule({(in_domain.dark, in_dummy.dummy) : out_domain.dark})
    R2 = Rule({(in_domain.medium, in_dummy.dummy) : out_domain.medium})
    R3 = Rule({(in_domain.light, in_dummy.dummy) : out_domain.light})

    rules = R1 | R2 | R3

    out_image = np.ndarray(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out_image[i,j] = rules({in_domain: img[i,j], in_dummy: 1})
    
    results = []
    for i in range(255):
        results.append(rules({in_domain: i, in_dummy: 1}))

    plt.figure()
    plt.title('Well, well, well')
    plt.plot(results)

    plt.figure()
    in_domain.dark.plot()
    in_domain.medium.plot()
    in_domain.light.plot() 

    plt.figure()
    out_domain.dark.plot()
    out_domain.medium.plot()
    out_domain.light.plot() 

    return out_image

def dark(x:int, high: int, lim: int, highval: int = 1):
    if x < high: return highval
    elif x < lim: return highval * (1 - 1.*(x-high)/(lim - high))
    else: return 0

def light(x:int, high: int, lim: int, highval: int = 1):
    if x > high: return highval
    elif x > lim: return highval * 1. * (x-lim)/(high-lim)
    else: return 0

def medium(x:int, l_lim:int, l_high:int, r_high:int, r_lim:int, highval:int = 1):
    if x < r_high: return light(x, l_high, l_lim, highval)
    else: return dark(x, r_high, r_lim, highval)

def fuzzy_contrast_enchancer_2(img: cv2.Mat, lvls_out: int = 511, new_black:int = 0, new_gray: int = 255, new_white:int = 511):

    black = np.min(img)
    white = np.max(img)
    gray = (black + white) / 2

    out_image = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out_image[i,j] = ( dark(img[i,j], (gray-black)/3, (gray-black)*5/6) * new_black +
                               medium(img[i,j], (gray-black)/3, (gray-black)*5/6, (white-gray)/6 + gray, (white-gray)*5/6 + gray) * new_gray +
                               light(img[i,j], (white-gray)/6 + gray, (white-gray)*2/3 + gray) * new_white ) / (
                               dark(img[i,j], (gray-black)/3, (gray-black)*5/6) +
                               medium(img[i,j], (gray-black)/3, (gray-black)*5/6, (white-gray)/6 + gray, (white-gray)*5/6 + gray) +
                               light(img[i,j], (white-gray)/6 + gray, (white-gray)*2/3 + gray) )

    return out_image
    
# https://www.cambridge.org/core/journals/apsipa-transactions-on-signal-and-information-processing/article/fullyautomatic-inverse-tone-mapping-algorithm-based-on-dynamic-midlevel-tone-mapping/3E58E1A14BC6543EB47B6C3B1A172C96

# Primitivno resenje:
def increase_num_levels(img: cv2.Mat) -> np.ndarray:
    noise = np.random.randint(0,0.1*(np.max(img) - np.min(img)), img.shape)
    return img + noise




if __name__ == '__main__':
    img = cv2.imread("../IMGS/INPUT/einstein.png")

    vals, hists = get_histogram(img)
    plot_multi_histogram(vals, hists, title='Original image histogram')

    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('UnLUTed')

    # 3a)

    lut = generate_lut(sigmoid)
    lut_img = apply_custom_LUT(img, lut)

    plt.figure()
    plt.imshow(cv2.cvtColor(lut_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('LUTed')

    lut_vals, lut_hists = get_histogram(lut_img)
    plot_multi_histogram(lut_vals, lut_hists, title='LUTed image histogram')

    # 3b)

    img_bw = bgr2grayscale(img)
    vals, _ = get_histogram(img_bw)
    print("Number of levels in original image: ", len(vals))
    plt.figure()
    plt.title('Original, grayscale')
    plt.imshow(img_bw, cmap='gray')

    img_deeper = increase_num_levels(img_bw)
    plt.figure()
    plt.title('Extended levels range')
    plt.imshow(img_deeper, cmap='gray')
    vals, _ = get_histogram(img_deeper)
    print("Number of levels in \"deepened\" image: ", len(vals))

    deeper_lut = generate_lut(sigmoid, np.min(img_deeper), np.max(img_deeper)+1)
    img_deeper_luted = apply_custom_LUT(img_deeper, deeper_lut)
    plt.figure()
    plt.title('Extended levels range with LUT applied')
    plt.imshow(img_deeper_luted, cmap='gray')
    vals, _ = get_histogram(img_deeper)
    print("Number of levels in \"deepened\" image, LUT-ed: ", len(vals))
    
    plt.show()