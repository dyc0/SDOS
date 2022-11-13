'''
 * 4. Napisati funkciju koja učitava RGB sliku po ličnom izboru i prikazuje informacije o
 * slici. Nakon toga razdvojiti R, G i B komponente slike i prikazati sve slike istovremeno
 * u jednom prozoru. Komponentu po izboru sačuvati kao intenzitetnu sliku. Početnu RGB sliku
 * konvertovati u indeksnu, prikazati je i sačuvati kao novu sliku. Prikazati polaznu sliku
 * kao sliku u ogledalu originalne slike po proizvoljno izabranoj osi i naznačiti koja je
 * osa izabrana.
'''


# Using OpenCV

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

def close_event():
    plt.close()
    print('CLOSED')

if __name__ == '__main__':

    # Load image
    img = cv.imread('IMGS/MrBean.jpg', cv.IMREAD_COLOR)

    # Show original image
    plt.figure(0)
    plt.axis('off')
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title('ORIGINAL')
    plt.draw()
    #plt.show()
    # NOTE: For some reason, cv.imshow freezes my console.

    # Split channels
    B, G, R = cv.split(img)
    channels = {1:R, 2:G, 3:B}
    names = {1:'RED', 2:'GREEN', 3:'BLUE'}
    plt.figure(1)
    for key in channels.keys():
        plt.subplot(1,3,key)
        plt.axis('off')
        plt.imshow(channels[key], cmap='gray')
        plt.title(names[key])
    #plt.show()

    # Save channel as intensity
    plt.figure(2)
    plt.imshow(channels[1], cmap='gray')
    plt.axis('off')
    plt.savefig('IMGS/red_chl_py.jpg')

    # Image quantization
    # Code taken from https://stackoverflow.com/questions/11064454/adobe-photoshop-style-posterization-and-opencv
    # This is great python code...
    n = 4
    indices = np.arange(0,256)
    divider = np.linspace(0,255,n+1)[1]
    quantiz = np.int0(np.linspace(0,255,n))
    color_levels = np.clip(np.int0(indices/divider),0,n-1)
    palette = quantiz[color_levels]             # B E A U T I F U L !!!
    img_quantized = palette[img]                # Palette method is faster and shorter!!!
    img_quantized = cv.convertScaleAbs(img_quantized)

    plt.figure(3)
    plt.axis('off')
    plt.imshow(cv.cvtColor(img_quantized, cv.COLOR_BGR2RGB))
    plt.savefig('IMGS/img_quantized_py.jpg')
    plt.title('QUANTIZED')

    # Mirroring
    img_flipped_x = cv.flip(img, 0) # 0 -> x, >0 -> y, <0 -> xy

    plt.figure(4)
    plt.axis('off')
    plt.imshow(cv.cvtColor(img_flipped_x, cv.COLOR_BGR2RGB))
    plt.title('FLIPPED AROUND X')
    plt.show()
