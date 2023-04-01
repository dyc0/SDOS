#! /usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt

def ideal_highpass(img, size):
    h, w   = img.shape[0:2]
    h1, w1 = int(h/2), int(w/2)
    img[h1-int(size/2):h1+int(size/2), w1-int(size/2):w1+int(size/2)] = 0
    return img

def inverse_transform_image(dft_img):
    idft_shift = np.fft.ifftshift(dft_img)
    return np.abs(np.fft.ifft2(idft_shift))


if __name__ == '__main__':

    # Import image and convert to grayscale
    img = cv2.imread('../IMGS/INPUT/MrBean.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Fourier transform
    img_dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(img_dft)

    # High-pass filter
    dft_shift = ideal_highpass(dft_shift, 25)
    res = np.log(np.abs(dft_shift))

    # Inverse Fourier transform
    idft = inverse_transform_image(dft_shift)
    
    plt.figure()
    plt.imshow(idft, cmap='gray')
    plt.title('Highpass')



    plt.show()