#! /usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import threshold_multiotsu

if __name__ == '__main__':

    img = cv2.imread("../IMGS/INPUT/Slika 03.bmp")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    og_hist, og_bins = np.histogram(img, 256)

    # Blurovana slika za poboljsavanje segmentacije
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img,-1,kernel)

    # Izdvajanje ivica sa dilatacijom
    edges = cv2.Canny(img, 50, 150)
    kernel = np.ones((3,3), dtype=np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    edged_image = cv2.bitwise_and(img, edges) 
    
    # Histogram za multiotsu se gradi na ivicama
    hist, bins = np.histogram(edged_image, 256)

    # Konacno, threshold sa 4 klase
    thresholds = threshold_multiotsu(dst, classes=4, hist=hist)
    regions = np.digitize(img, bins=thresholds)

    # Calculate median, assume it is part of background, and then remove it
    bg_region = np.argmax(thresholds > np.median(img))+1
    regions = regions + 1
    regions[regions == bg_region] = 0
    regions[regions > 0] = 1
    regions = np.array(regions, dtype=np.uint8)
    
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,1))
    regions = cv2.morphologyEx(regions, cv2.MORPH_CLOSE, kernel)
    
    ff_kernel = np.zeros((regions.shape[0]+2, regions.shape[1]+2), np.uint8)
    ff_regions = regions.copy()
    cv2.floodFill(ff_regions, ff_kernel, (0,0), 255)
    ff_regions = cv2.bitwise_not(ff_regions)

    regions = regions | ff_regions

    # Slike
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(img, cmap='gray')
    plt.title('Original')
    plt.axis('off')
    plt.subplot(1,2,2)
    plt.imshow(regions, cmap='gray')
    plt.title('Multi-Otsu result')
    plt.axis('off')

    # Overlap
    plt.figure()
    plt.imshow(cv2.bitwise_and(img, img, mask=regions), cmap='gray')
    plt.title("Overlap")
    plt.axis("off")

    # Histogram za multiotsu
    plt.figure()
    plt.plot(og_bins[:-1],og_hist)
    plt.title('Histogram')
    for thresh in thresholds:
        plt.axvline(thresh, color='r')

    plt.show()
