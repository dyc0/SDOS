# VERSION WITHOUT LOOPS

import numpy as np

_DIMENSION = 1024

def isinteger(I: np.matrix) -> None:
    return np.round(I) == I


if __name__ == '__main__':
    I = np.random.uniform(-10, 10, (_DIMENSION, _DIMENSION))
    isinteger(I)
