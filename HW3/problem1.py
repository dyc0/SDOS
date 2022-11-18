'''
These are actually hws 3/1 and 3/2.
'''

import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

import HISTOGRAM_LIB as hl

# This is not da Python wae:
def get_histogram_full_8bit(img: cv2.Mat) -> list:
    vals, hists = hl.get_histogram(img)

    newhists = []
    for val_arr, hist_arr in zip(vals, hists):
        newhist = np.zeros(256)
        newhist[val_arr] = hist_arr
        newhists.append(newhist)

    return newhists

def cumulate_hist(hist: np.ndarray, numpx:int = -1) -> np.ndarray:
    # Suppose 8-bit one-channel
    sum = 0
    lut = np.zeros(256)
    if numpx < 0: numpx = np.sum(hist)
    for ind, val in enumerate(hist):
        sum += float(val)/numpx
        lut[ind] = int(sum*255)
    return lut.astype('uint8')

def cumulate_multi_hist(hist: list, numpx:int = -1) -> np.ndarray:
    luts = []
    for hs in hist:
        luts.append(cumulate_hist(hs, numpx))
    luts = np.dstack(luts)
    return luts

def apply_lut(img: cv2.Mat, lut:np.ndarray) -> cv2.Mat:
    assert(len(img.shape) == len(lut.shape)) # TODO: Check if correct

    if len(img.shape) == 3:
        b,g,r = cv2.split(img)
        b_lut, g_lut, r_lut = np.split(lut, 3, axis=2)
        b_new = b_lut.flatten()[b]
        g_new = g_lut.flatten()[g]
        r_new = r_lut.flatten()[r]
        return cv2.merge((b_new, g_new, r_new))
    elif len(img.shape) == 2:
        return lut[img]
    else:
        return 0

def log_transform(c: float = 1) -> float:
    return lambda x: c*math.log(1+x)

def gama_transform(gamma:float = 1, c:float = 1) -> float:
    return lambda x: c * x**gamma


if __name__ == '__main__':
    img = cv2.imread('MrBean.jpg')

    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original')
    vals0, hists0 = hl.get_histogram(img)
    hl.plot_multi_histogram(vals0, hists0)

    # Using cv2 equalization: (PROBLEM 1a)
    b, g, r = cv2.split(img)
    eh_r = cv2.equalizeHist(r)
    eh_g = cv2.equalizeHist(g)
    eh_b = cv2.equalizeHist(b)

    img_cv = cv2.merge((eh_b, eh_g, eh_r))
    plt.figure()
    plt.imshow(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    plt.title('Equalized, OpenCV')
    vals_cv, hists_cv = hl.get_histogram(img_cv)
    hl.plot_multi_histogram(vals_cv, hists_cv, title='Equalized histogram, OpenCV')

    # PROBLEM 1b
    img_ue = cv2.imread('MrBean_UE.jpg')
    vals_ue, hist_ue = hl.get_histogram(hl.normalize01(img_ue))
    hl.plot_multi_histogram(vals_ue, hist_ue, title='Underexposed')
    hl.show_image(img_ue, title='Underexposed')

    lut_log = hl.generate_lut(log_transform(1))
    img_log = cv2.LUT(img_ue, lut_log)
    img_log = hl.normalize01(img_log)              # Normalization nullifies the usage of c in log

    vals_log, hist_log = hl.get_histogram(img_log)
    hl.plot_multi_histogram(vals_log, hist_log, title="Log histogram")
    hl.show_image(img_log, title="Log")

    lut_gamma = hl.generate_lut(gama_transform(0.5))
    img_gamma = cv2.LUT(img_ue, lut_gamma)
    img_gamma = hl.normalize01(img_gamma)

    vals_gamma, hist_gamma = hl.get_histogram(img_gamma)
    hl.plot_multi_histogram(vals_gamma, hist_gamma, title="Gamma histogram")
    hl.show_image(img_gamma, title="Gamma")

    # Using my equalization: (PROBLEM 2)
    hist = get_histogram_full_8bit(img)
    luts = cumulate_multi_hist(hist)
    img_my_eq = apply_lut(img, luts)

    plt.figure()
    plt.imshow(cv2.cvtColor(img_my_eq, cv2.COLOR_BGR2RGB))
    plt.title('Equalized, mine')
    vals_my, hists_my = hl.get_histogram(img_my_eq)
    hl.plot_multi_histogram(vals_my, hists_my, title='Equalized histogram, my method')

    plt.show()