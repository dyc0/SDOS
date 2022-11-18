'''
(a) Napisati funkciju za lokalnu ekvalizaciju histograma. Definiše se prozor 3x3 koji se pomera pixel po pixel.
Unutar prozora se izračunava histogram i primenjuje se ekvalizacija. Vrednost centralnog piksela se zamenjuje novom vrednošću.
Prozor se pomera za jedan pixel i postupak se ponavlja.

(b) Na osnovu odabrane objektivne metrike napraviti poređenje između globalne i lokalne primene ekvalizacije iz dela (a).
'''

import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

import HISTOGRAM_LIB as hl
from problem1 import get_histogram_full_8bit

