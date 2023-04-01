#! /usr/bin/python

# Using PIL library

from PIL import Image
from matplotlib import pyplot as plt

if __name__ == '__main__':

    # LOAD IMAGE
    with (Image.open('../IMGS/INPUT/MrBean.jpg') as img):

        # SHOW IMAGE
        img.show()

        # PRINT INFO
        print('IMAGE INFORMATION')
        print('filename: ' + img.filename)
        print('format: ' + img.format)
        print('mode: ' + img.mode)
        print('size:' + str(img.size))
        print('width: ' + str(img.width))
        print('height: ' + str(img.height))
        print('palette: ' + str(img.palette))
        for k in img.info.keys():
            if k in ['photoshop', 'icc_profile', 'exif']: continue
            print(str(k) + ":" + str(img.info[k]))

        # SPLIT CHANNELS AND SAVE
        red, green, blue = img.split()
        red.save('../IMGS/OUTPUT/MrBean_red_channel.jpg')

        plt.figure()

        plt.subplot(1,3,1)
        plt.imshow(red, cmap='Reds_r')
        plt.title('RED')

        plt.subplot(1,3,2)
        plt.imshow(green, cmap='Greens_r')
        plt.title('GREEN')
        
        plt.subplot(1,3,3)
        plt.imshow(blue, cmap='Blues_r')
        plt.title('BLUE')

        # INDEX IMAGE
        index_img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=8)
        index_img.save('../IMGS/OUTPUT/MrBean_index.png')
        plt.figure()
        plt.imshow(index_img)
        plt.title('INDEX')

        # FLIPPING
        flip_img = img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        plt.figure()
        plt.imshow(flip_img)
        plt.title('FLIPPED AROUND Y-AXIS')

        plt.show()