import numpy as np
import math

def gaussian(x, amp, centroid, sigma):
    return amp / np.sqrt(2 * math.pi * sigma**2) * \
            np.exp(-(x-centroid)**2 / (2 * sigma**2))

def gaussian_linear(x, amp, centroid, sigma, a, b):
    return a*x + b + gaussian(x, amp, centroid, sigma)