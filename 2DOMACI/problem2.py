# IMAGE NORMALIZATION 

from problem1 import bgr2grayscale, get_histogram, plot_histogram

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
    img = cv2.imread('MrBean_OE.jpg')

    gs_img = bgr2grayscale(img)
    gs_vals, gs_hist = get_histogram(gs_img)
    
    plt.figure()
    plt.imshow(gs_img, cmap='gray', vmin=0, vmax=255)
    plt.title('Before normalizing')
    plot_histogram(gs_vals, gs_hist, title='Grayscale histogram')

    norm = normalize01(gs_img)
    norm_vals, norm_hist = np.unique(norm, return_counts=True)

    plt.figure()
    plt.imshow(norm, cmap='gray', vmin=0, vmax=1)
    plt.title('After normalizing')
    plot_histogram(norm_vals, norm_hist, title='Normalized image histogram')

    plt.show()