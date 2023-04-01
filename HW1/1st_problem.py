#! /usr/bin/python

import numpy as np

DIMENSION = 1024

def isinteger(I: np.matrix) -> None:
    return np.round(I) == I


if __name__ == '__main__':
    I = np.random.uniform(-10, 10, (DIMENSION, DIMENSION))
    isinteger(I)
