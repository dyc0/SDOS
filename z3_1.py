import numpy as np
from matplotlib import pyplot as plt

def y(x, a=0.5, b=10):
    return 1./(1 + 1./(x+a)**b)

xs = np.arange(0,10,0.01)
ys = [y(x,0.2,4) for x in xs]
plt.plot(xs,ys)
plt.show()