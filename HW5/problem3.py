#! /usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import threshold_multiotsu

def segment_image(path):
    o_img = cv2.imread(path)
    img = cv2.cvtColor(o_img, cv2.COLOR_BGR2GRAY)
    og_hist, og_bins = np.histogram(img, 256)
    
    # Blurovana slika za poboljsavanje segmentacije
    kernel = np.ones((20,20), np.float32)
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
    
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    regions = cv2.morphologyEx(regions, cv2.MORPH_OPEN, kernel)
   
    ff_kernel = np.zeros((regions.shape[0]+2, regions.shape[1]+2), np.uint8)
    ff_regions = regions.copy()
    cv2.floodFill(ff_regions, ff_kernel, (0,0), 255)
    ff_regions = cv2.bitwise_not(ff_regions)
    
    regions = regions | ff_regions

    contours, hierarchy = cv2.findContours(regions, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(o_img, contours, -1, (0, 255, 0), 1)

    plt.figure()
    plt.title("Segmented objects")
    plt.imshow(cv2.cvtColor(o_img, cv2.COLOR_BGR2RGB))


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

if __name__ == '__main__':
    segment_image("../IMGS/INPUT/Slika 03.bmp")
    segment_image("../IMGS/INPUT/Slika 04.bmp")

    plt.show()
