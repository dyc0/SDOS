'''
(a) Napisati funkciju zasnovanu na odabranoj nelinearnoj ulazno-izlaznoj karakteristici
    čijom primenom se intenziteti ulazne slike konvertuju u opseg [0,1]. Prikazati 
    odgovarajući histogram pre i posle primene funkcije.

(b) Za ulaznu osmobitnu sliku po izboru povećati amplitudsku rezoluciju,
    odnosno predstaviti sliku sa brojem različitih nivoa koji je veći od 256.
    Pokazati na automatizovan način koliko se različitih nivoa sive koristilo pre i 
    posle povećanja amplitudske rezolucije. Napisati funkciju iz (a) tako da se može 
    koristiti i ulazna slika sa kodnom reči koja je veća od osam bita.
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

from problem1 import get_histogram, plot_multi_histogram, plot_histogram

def sigmoid(x: float, scale:float = 25., center:float = 125.) -> float:
    return 1/(1+math.exp(-(x-center)/scale))

def generate_lut(func: callable, begin: int = 0, end: int = 256) -> np.array:
    val_range = np.arange(begin, end)
    func_vect = np.vectorize(func)
    return func_vect(val_range).astype('float32')

def widen_amp_res(lvl_in: int = 8, lvl_out: int = 16):
    inrange = np.arange(2**lvl_in)
    outrange = np.arange(2**lvl_out)
    
    

if __name__ == '__main__':
    img = cv2.imread("MrBean.jpg")

    vals, hists = get_histogram(img)
    plot_multi_histogram(vals, hists, title='Original image histogram')

    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('UnLUTed')

    lut = generate_lut(sigmoid)
    lut_img = cv2.LUT(img, lut)

    plt.figure()
    plt.imshow(cv2.cvtColor(lut_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('LUTed')

    lut_vals, lut_hists = get_histogram(lut_img)
    plot_multi_histogram(lut_vals, lut_hists, title='LUTed image histogram')



    
    plt.show()