import cv2 as cv
from matplotlib import pyplot as plt

if __name__ == '__main__':

    # Load image
    img = cv.imread('../MrBean.jpg', cv.IMREAD_COLOR)

    # Show original image
    plt.figure()
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title('ORIGINAL')
    plt.show()
    # NOTE: For some reason, cv.imshow freezes my console.