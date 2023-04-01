#! /usr/bin/python

# IMAGE NORMALIZATION 

from problem1 import bgr2grayscale, get_histogram, plot_histogram, plot_multi_histogram

import cv2
import numpy as np
from matplotlib import pyplot as plt

def normalize01(img: cv2.Mat) -> np.array:
    min = np.min(img)
    max = np.max(img) - min

    normalized = img - min
    normalized = np.divide(normalized, max)

    return normalized

if __name__ == '__main__':
    img = cv2.imread('../IMGS/INPUT/MrBean_OE.jpg')


    # GRAYSCALE
    gs_img = bgr2grayscale(img)
    gs_vals, gs_hist = get_histogram(gs_img)
    
    plt.figure()
    plt.imshow(gs_img, cmap='gray', vmin=0, vmax=255)
    plt.title('Before normalizing')
    plot_histogram(gs_vals, gs_hist, title='Grayscale histogram')


    # NORMALIZED
    norm = normalize01(gs_img)
    norm_vals, norm_hist = np.unique(norm, return_counts=True)

    plt.figure()
    plt.imshow(norm, cmap='gray', vmin=0, vmax=1)
    plt.title('After normalizing')
    plot_histogram(norm_vals, norm_hist, title='Normalized image histogram')


    # ORIGINAL RGB
    o_vals, o_hist = get_histogram(img)
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original RGB')
    plot_multi_histogram(o_vals, o_hist, title='Original image histogram')

    plt.show()