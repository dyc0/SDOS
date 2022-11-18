# VERSION WITHOUT LOOPS

import numpy as np

_DIMENSION = 1024

def iseven(I: np.matrix) -> None:
    return I % 2 == 0


if __name__ == '__main__':
    I = np.random.randint(-10, 10, (_DIMENSION, _DIMENSION))
    iseven(I)
    
