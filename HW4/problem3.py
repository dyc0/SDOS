#! /usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt
from HISTOGRAM_LIB import show_image

def results(fft_img, title, filt=None):
    if filt is not None:
        filt_img = fft_img * filt
        rs = 2
    else:
        rs = 1
        filt_img = fft_img

    img_amp = np.abs(filt_img)
    img_phase = np.angle(filt_img)

    image = inverse_transform(filt_img)
    show_image(image, title)
    
    print(title)
    print("STDEV: " + str(np.std(image)))
    print("CONTRAST: " + str((np.max(image) - np.min(image)) / (np.max(image) + np.min(image))))
    
    plt.figure()
    plt.subplot(rs,2,1)
    plt.imshow(np.log(1+img_amp), cmap='gray')
    plt.title(title + ", amplitudski spektar")
    plt.subplot(rs,2,2)
    plt.imshow(img_phase, cmap='gray')
    plt.title(title + ", fazni spektar")
    if filt is not None:
        plt.subplot(2,2,3)
        plt.imshow(np.log(1+abs(filt)), cmap='gray')
        plt.title(title + ", amplitudska karakteristika")
        plt.subplot(2,2,4)
        plt.imshow(np.angle(filt), cmap='gray')
        plt.title(title+", fazna karakteristika")

def inverse_transform(filtered_image):
    filtered_image_shift = np.fft.ifftshift(filtered_image)
    filtered_image_inverse = np.fft.ifft2(filtered_image_shift)
    filtered_image_inverse = np.abs(filtered_image_inverse)  # Take the absolute value
    filtered_image_inverse = filtered_image_inverse.astype(np.uint8)

    return filtered_image_inverse

if __name__ == '__main__':
    
    # SLIKA
    img = cv2.imread('../IMGS/INPUT/MrBean.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fft_img = np.fft.fft2(img)
    fshift = np.fft.fftshift(fft_img)
    
    results(fshift, "Originalna")

    # SUM
    mean = 0
    stddev = 80
    noise = np.zeros(img.shape, np.uint8)
    cv2.randn(noise, mean, stddev)
    noise = np.array(noise*0.2, dtype=np.uint8)    

    img = img+noise

    fft_img = np.fft.fft2(img)
    fshift = np.fft.fftshift(fft_img)

    results(fshift, "Sumovita")

    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2  # center coordinates

    x = np.linspace(-ccol, ccol - 1, cols)
    y = np.linspace(-crow, crow - 1, rows)
    X, Y = np.meshgrid(x, y)
    dist = np.sqrt(X**2 + Y**2)

    laplace_filt = np.zeros((rows, cols))
    laplace_filt[crow-1:crow+2, ccol-1:ccol+2] = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    laplace_filt=np.fft.fftshift(np.fft.fft2(laplace_filt))

    sigma=2
    homeomorph = 1 - np.exp(-dist**2/(2*sigma**2))

    results(fshift, "Laplace filtering", laplace_filt)
    results(fshift, "Homeomorph filtering", homeomorph)

    # Homeomorfno filtriranje uspelo je da izdvoji visoke frekvencije uz manje suma, dok je Laplas ostao vrlo osetljiv na dodati sum.

    plt.show()
