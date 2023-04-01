# HISTOGRAM IMPLEMENTATION

from matplotlib import pyplot as plt
import numpy as np
import cv2

def bgr2grayscale (img: cv2.Mat) -> np.array:
    return np.asarray((114./1000*img[:,:,0] + 587./1000*img[:,:,1] + 299./1000*img[:,:,0]), dtype = int)

def get_histogram(img: cv2.Mat):
    # If image is grayscale:
    if len(img.shape) < 3: return np.unique(img, return_counts=True)

    # If image is multi-channel:
    vals = []
    hists = []
    for i in range(img.shape[2]):
        val, hist = np.unique(img[:,:,i], return_counts=True)
        vals.append(val)
        hists.append(hist)
    return vals, hists

def plot_histogram(xaxis: np.array, histogram: np.array, title: str = 'Histogram', xlabel: str = 'Pixel value', ylabel: str = 'No. of pixels', normalize: bool = False) -> None:
    if normalize:
        h2s = histogram/np.sum(histogram)
        ylabel = 'Percentage of pixels'
    else: h2s = histogram
    plt.figure()
    plt.plot(xaxis, h2s) 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

def plot_multi_histogram(vals: list, hists: list,
                       title: str = 'Histogram', xlabel: str = 'Pixel value', ylabel: str = 'No. of pixels', normalize: bool = False) -> None:
    assert(len(vals)==len(hists))

    plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if normalize: hists_to_plot = [hist / np.sum(hist) for hist in hists]
    else: hists_to_plot = hists
    if len(vals) == 3:
        colors = ['blue', 'green', 'red']
        for val, hist, col in zip(vals, hists_to_plot, colors):
            plt.plot(val, hist, color=col)
    else:
        for val, hist in zip(vals, hists_to_plot):
            plt.plot(val, hist)

def normalize01(img: cv2.Mat) -> np.array:
    min = np.min(img)
    max = np.max(img) - min

    normalized = img - min
    normalized = np.divide(normalized, max)

    return normalized

def generate_lut(func: callable, begin: int = 0, end: int = 256) -> np.array:
    val_range = np.arange(begin, end)
    func_vect = np.vectorize(func)
    return func_vect(val_range).astype('float32')


def show_image(img: cv2.Mat, title: str = "", axis: bool = False) -> None:
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not axis: plt.axis('off')
    plt.title(title)