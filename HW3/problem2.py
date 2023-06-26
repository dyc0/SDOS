#! /usr/bin/python

from HISTOGRAM_LIB import show_image, get_histogram, plot_histogram
import numpy as np
import cv2
from matplotlib import pyplot as plt

def direct_eq(I):
    lvls = 256
    (x, y) = I.shape
    n = x*y

    nks, vals = np.histogram(I, np.arange(256))
    vals = vals[:-1]
    
    outs = np.zeros(lvls)
    outs[0] = nks[0]*1.0/n*(lvls - 1)
    for i in range(1, len(nks)):
        outs[i] = outs[i-1]*n + float(nks[i])
        outs[i] = outs[i]/n

    return np.array(outs[I]*255, dtype=np.uint8)



if __name__ == '__main__':
    img = cv2.imread('../IMGS/INPUT/MrBean.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    show_image(img, "Original")
    vals, hists = get_histogram(img)
    plot_histogram(vals, hists, title="Original histogram")

    eqd = direct_eq(img)
    show_image(eqd, "Equalized")
    vals, hists = get_histogram(eqd)
    plot_histogram(vals, hists, title="Equalized histogram")

    plt.show()
