#! /usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt

import HISTOGRAM_LIB as hl
from problem1 import get_histogram_full_8bit, cumulate_multi_hist

def pixel_apply_lut(px:np.ndarray, lut:np.ndarray) -> np.ndarray:
    """Applies given LUT to a single pixel.

    Args:
        px (np.ndarray): 8-bit BGR pixel.
        lut (np.ndarray): LUT for 8-bit BGR.

    Returns:
        np.ndarray: Pixel with the LUT applied.
    """

    return np.array([lut[0, px[0], 0], lut[0, px[1], 1], lut[0, px[2], 2]])

def pixel_eq(img: cv2.Mat, wx: int = 3, wy:int = 3) -> cv2.Mat:
    """Performs a pixel-by-pixel local histogram equalization.

    The image is iterated through pixel by pixel. LUT for histogram
    equalization is calculated for the neighbourhood of each pixel.
    The dimensions of the neighbourhood are (wx, wy) if wx, wy are odd
    and (wx+1, wy+1) if they are even. The LUT is the applied to the
    pixel in the centre of the neighbourhood.

    Args:
        img (cv2.Mat): Image to be equalized.
        wx (int, optional): Width of pixel neghbourhood. Defaults to 20.
        wy (int, optional): Height of pixel neghbourhood. Defaults to 20.

    Returns:
        cv2.Mat: Equalized image.
    """

    dim_x = img.shape[0]
    dim_y = img.shape[1]
    # Border is added to source image to reduce edge effects. Pixels on
    # the edge are repeated.
    src_img = cv2.copyMakeBorder(img,
                                 top=wy//2, bottom=wy//2,
                                 left=wx//2, right=wy//2,
                                 borderType=cv2.BORDER_REPLICATE)
    lut_img = img.copy()
    
    for x in range(wx//2, dim_x+wx//2):
        for y in range(wy//2, dim_y+wy//2):
            window = src_img[x-wx//2:x+wx//2, y-wy//2:y+wy//2]
            lut = cumulate_multi_hist(get_histogram_full_8bit(window))
            # lut_img does not have borders
            lut_img[x-wx//2,y-wy//2,:] = pixel_apply_lut(lut_img[x-wx//2,y-wy//2], lut)

    return lut_img

def adaptive_eq(img: cv2.Mat, wx: int = -1, wy:int = -1) -> cv2.Mat:
    """Function performs adaptive histogram equalization.

    Args:
        img (cv2.Mat): _description_
        wx (int, optional): Width of equalization window. Defaults to
        -1, which means that the width of image_width//4 is used.
        wy (int, optional): Height of equalization window. Defaults to
        -1, which means that the height of image_height//4 is used.

    Returns:
        cv2.Mat: Equalized image.
    """

    if wx == -1: wx = img.shape[0] // 4
    if wy == -1: wy = img.shape[1] // 4

    lut_img = img.copy()

    for x in range(0, img.shape[0], wx):
        for y in range(0, img.shape[1], wy):
            window = img[x:x+wx, y:y+wy]
            lut = cumulate_multi_hist(get_histogram_full_8bit(window))
            lut_img[x:x+wx, y:y+wy, :] = cv2.LUT(window, lut)

    return lut_img

def get_contrast(img: cv2.Mat) -> list:
    """Function returns max-min value for B, G, and R channels
    in a list.

    Args:
        img (cv2.Mat): 8-bit BGR OpenCV image.

    Returns:
        list: List of B, G and R contrasts
    """

    return [(np.max(img[:,:,0])-np.min(img[:,:,0]))/255., 
            (np.max(img[:,:,1])-np.min(img[:,:,1]))/255.,
            (np.max(img[:,:,2])-np.min(img[:,:,2]))/255.]

def get_snr(img: cv2.Mat) -> list:
    """Returns SNR for each channel of the image.

    Args:
        img (cv2.Mat): BGR OpenCV image.

    Returns:
        list: List of B, G and R SNRs.
    """

    return [np.average(img[:,:,0])*1./np.std(img[:,:,0]),
            np.average(img[:,:,1])*1./np.std(img[:,:,1]),
            np.average(img[:,:,2])*1./np.std(img[:,:,2])]

def get_ffts(img:cv2.Mat, title:str) -> None:
    plt.figure()
    plt.title(title)
    for sp, name, chann in zip([1, 2, 3], ["Blue", "Green", "Red"], [img[:,:,0], img[:,:,1], img[:,:,2]]):
        red = np.abs(np.fft.fft2(chann))
        plt.subplot(1,3,sp)
        plt.plot(red)
        plt.title(name)

def print_parameters(img: cv2.Mat, title: str, plot_hist:bool = False):
    print("PARAMETERS FOR " + title)
    contrast = get_contrast(img)
    print("Contrast:\n\tR = {red}\tG = {green}\tB = {blue}".format(red=contrast[2], green=contrast[1], blue=contrast[0]))
    snr = get_snr(img)
    print("SNR:\n\tR = {red}\tG = {green}\tB = {blue}".format(red=snr[2], green=snr[1], blue=snr[0]))
    vals, hists = hl.get_histogram(img)
    if plot_hist: hl.plot_multi_histogram(vals, hists, title=title)
    print("Histogram snr:\n\tR = {red}\tG = {green}\tB = {blue}".format(
        red=np.average(hists[2])/np.std(hists[2]),
        green=np.average(hists[1])/np.std(hists[1]),
        blue=np.average(hists[0])/np.std(hists[0])))
    print("\n")

if __name__ == "__main__":
    plot_hist = True

    img = cv2.imread('../IMGS/INPUT/MrBean.jpg')
    hl.show_image(img, title="Original image")
    print_parameters(img, "Original image", plot_hist)

    # 3.A & B - Histogram equalization, local, adaptive and global, and comparison

    ## LOCAL
    img_pe = pixel_eq(img)
    hl.show_image(img_pe, title="Pixel-histogram-eq")
    print_parameters(img_pe, "Pixel-histogram-eq", plot_hist)

    ## ADAPTIVE
    img_ae = adaptive_eq(img)
    hl.show_image(img_ae, title="Adaptive histogram eq")
    print_parameters(img_ae, "Adaptive histogram eq", plot_hist)

    ## GLOBAL
    img_ge = cv2.LUT(img, cumulate_multi_hist(get_histogram_full_8bit(img)))   
    hl.show_image(img_ge, title="Global histogram eq")
    print_parameters(img_ge, "Global histogram eq", plot_hist)

    plt.show()
    exit(0)