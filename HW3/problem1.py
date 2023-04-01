#! /usr/bin/python

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
    """Gets histogram for 8-bit image as an array.

    Function uses previously implemented get_histogram to calculate
    histogram, populates the histogram array with zeros where values
    are missing.

    Args:
        img (cv2.Mat): A BGR or grayscale OpenCV image whose histogram is needed.

    Returns:
        list: A list of histograms for each channel.
    """

    vals, hists = hl.get_histogram(img)

    newhists = []
    for val_arr, hist_arr in zip(vals, hists):
        newhist = np.zeros(256)
        newhist[val_arr] = hist_arr
        newhists.append(newhist)

    return newhists

def cumulate_hist(hist: np.ndarray, numpx:int = -1) -> np.ndarray:
    """Calculates the cumulative sum of a given histogram.

    The sum is calculated for each histogram level l according to the
    formula     sum[l] = sum[l-bit-1] + histogram[l]/numpx * 255.   It is
    assumed that the image is 8-bit. If numpx is -1, then the number of
    pixels is calculated as a sum of a histogram.

    Args:
        hist (np.ndarray): A histogram.
        numpx (int, optional): Number of pixels in an image. Defaults to -1.

    Returns:
        np.ndarray: Cumulative sum of given histogram.
    """

    # Suppose 8-bit one-channel
    sum = 0
    lut = np.zeros(256)
    # If we do not pass the number of pixels explicitly:
    if numpx < 0: numpx = np.sum(hist)
    
    for ind, val in enumerate(hist):
        sum += float(val)/numpx
        lut[ind] = int(sum*255)
    return lut.astype('uint8')

def cumulate_multi_hist(hist: list, numpx:int = -1) -> np.ndarray:
    """Calculates cumulative sums of multiple histograms using repeated
    calls to cumulate_hist function.

    Args:
        hist (list): List of histograms
        numpx (int, optional): Number of pixels in an image. Defaults to -1.

    Returns:
        np.ndarray: Stacked array of cumulative sums ready to be used
        as a LUT.
    """

    luts = []
    for hs in hist:
        luts.append(cumulate_hist(hs, numpx))
    luts = np.dstack(luts)
    return luts

def apply_lut(img: cv2.Mat, lut:np.ndarray) -> cv2.Mat:
    """Function that applies a LUT to an image and returns a new one.

    Args:
        img (cv2.Mat): A BGR or grayscale OpenCV image.
        lut (np.ndarray): LUT.

    Returns:
        cv2.Mat: New image with LUT applied.
    """

    # There must be LUT for each channel:
    assert(len(img.shape) == len(lut.shape))

    # BGR images:
    if len(img.shape) == 3:
        b,g,r = cv2.split(img)
        b_lut, g_lut, r_lut = np.split(lut, 3, axis=2)
        b_new = b_lut.flatten()[b]
        g_new = g_lut.flatten()[g]
        r_new = r_lut.flatten()[r]
        return cv2.merge((b_new, g_new, r_new))
    # Grayscale images:
    elif len(img.shape) == 2:
        return lut[img]
    else:
        return 0

def log_transform(c: float = 1) -> float:
    return lambda x: c*math.log(1+x)

def gama_transform(gamma:float = 1, c:float = 1) -> float:
    return lambda x: c * x**gamma


if __name__ == '__main__':
    img = cv2.imread('../IMGS/INPUT/MrBean.jpg')

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
    img_ue = cv2.imread('../IMGS/INPUT/MrBean_UE.jpg')
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