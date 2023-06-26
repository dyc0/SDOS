#! /usr/bin/python

import numpy as np
import cv2
from matplotlib import pyplot as plt
from numpy.fft import fftshift
from scipy import ndimage
from HISTOGRAM_LIB import show_image 

if __name__ == "__main__":

    img = cv2.imread('../IMGS/INPUT/MrBean.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fft_img = np.fft.fft2(img)
    fshift = np.fft.fftshift(fft_img)

    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2  # center coordinates

    x = np.linspace(-ccol, ccol - 1, cols)
    y = np.linspace(-crow, crow - 1, rows)
    X, Y = np.meshgrid(x, y)
    dist = np.sqrt(X**2 + Y**2)

    cutoff_freq = 10

    # A. SEPARABLE FILTER
    separable_filter = np.double((X > cutoff_freq) | (Y > cutoff_freq))

    # B. CIRCULAR FILTER
    circular_filter = np.zeros((rows, cols))
    circular_filter[dist > cutoff_freq] = 1

    # C. PREWITT FILTER - SPACIAL DOMAIN
    spacial_prewitt_filtered = ndimage.prewitt(img)
    show_image(spacial_prewitt_filtered, title="Spacial PREWITT filter")
    show_image(cv2.Canny(spacial_prewitt_filtered, threshold1=30, threshold2=100), title="Spacial PREWITT edges")

    # D. PREWITT FILTER - FREQ DOMAIN
    prewitt_filter = np.zeros((rows, cols))
    prewitt_filter[crow-1:crow+2, ccol-1:ccol+2] = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    prewitt_filter=np.fft.fftshift(np.fft.fft2(prewitt_filter))



    for imgfilter, title in zip([separable_filter, circular_filter, prewitt_filter], ["SEPARABLE FILTER", "CIRCULAR FILTER", "PREWITT FILTER"]):
        filtered_image = fshift * imgfilter

        filtered_image_shift = np.fft.ifftshift(filtered_image)
        filtered_image_inverse = np.fft.ifft2(filtered_image_shift)
        filtered_image_inverse = np.abs(filtered_image_inverse)  # Take the absolute value
        filtered_image_inverse = filtered_image_inverse.astype(np.uint8)
        
        edge_image = cv2.Canny(filtered_image_inverse, threshold1=30, threshold2=100)

        show_image(filtered_image_inverse, title=title)
        show_image(edge_image, title=title+", edges")

    plt.show()
