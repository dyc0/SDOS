# NO FOR LOOPS

import numpy as np
from matplotlib import pyplot as plt

def draw_rectangle(dimx: int, dimy: int, rectx: int, recty: int) -> None:
    if dimx <= rectx or dimy <= recty:
        return np.zeros((dimx, dimy))
    
    frame = np.zeros((dimx, dimy))
    rectangle = np.ones((rectx, recty))
    frame[(dimx-rectx)//2:(dimx+rectx)//2, (dimy-recty)//2:(dimy+recty)//2] = rectangle
    return frame

def draw_triangle(dimx: int, dimy: int, halfbase: int) -> None:
    if dimx <= 2*halfbase or dimy <= 2*halfbase:
        return np.zeros((dimx, dimy))

    xx, yy = np.mgrid[-dimx//2:dimx//2, -dimy//2:dimy//2]
    triangle = ( (abs(xx) + abs(yy) < halfbase) * (xx < 0) ) * 1

    return triangle

def draw_circle(dimx: int , dimy: int, r: int) -> None:
    if dimx <= 2*r or dimy <= 2*r:
        return np.zeros((dimx, dimy))

    xx, yy = np.mgrid[-dimx//2:dimx//2, -dimy//2:dimy//2]
    circle = (xx**2 + yy**2 <= r**2) * 1
    return circle

if __name__ == '__main__':

    rectangle = draw_rectangle(1024, 2048, 512, 1024)
    plt.matshow(rectangle, cmap='gray')

    triangle = draw_triangle(2048, 2048, 1000)
    plt.matshow(triangle, cmap='gray')

    circle = draw_circle(2048, 2048, 512)
    plt.matshow(circle, cmap='gray')

    plt.show()