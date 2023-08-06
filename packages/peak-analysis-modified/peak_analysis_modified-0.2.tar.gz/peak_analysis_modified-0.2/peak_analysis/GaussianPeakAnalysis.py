import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from .PeakAnalysis import Peak
from .helper import gaussian, gaussian_linear

class GaussianPeak(Peak):
    def __init__(self, centroid, sigma, has_lin_bg=False):
        ''''''
        Peak.__init__(self, centroid, sigma)
        self.has_lin_bg = has_lin_bg
    
    def fit_gaussian(self):
        '''
        Fit gaussian with or without linear backgroud to the spectrum
        Updata the centroid and sigma parameters
        
        Return: fitting function
        '''
        # if there is no linear background, fit a gaussian to spectrum
        if self.has_lin_bg:
            params, _ = curve_fit(gaussian_linear, self.spectrum_x, self.spectrum_y, p0=[1, self.centroid, self.sigma, 0.1, 0.1],\
                                    bounds=([1, self.centroid-3, 0, -np.inf, -np.inf], [100000000, self.centroid+3, 10, np.inf, np.inf]))
            print(params)
            fit_y = [gaussian_linear(i, *params) for i in self.spectrum_x]
            self.plot_fit(fit_y)


        # if there is a linear background, fit gaussian+linear fucntion
        else:
            # fit_func = gaussian(self.spectrum_x, 10., 23., 1.)
            params, _ = curve_fit(gaussian, self.spectrum_x, self.spectrum_y, p0=[1, self.centroid, self.sigma],\
                                    bounds=([0, self.centroid-3, 0], [100000000, self.centroid+3, 5]))
            print(params)
            fit_y = [gaussian(i, *params) for i in self.spectrum_x]
            self.plot_fit(fit_y)

        # Updata centroid and sigma
        self.centroid = params[1]
        self.sigma = params[2]

    
    def plot_fit(self, fit_value):
        '''Visualize the fit on top of the spectrum
        '''
        plt.plot(self.spectrum_x, self.spectrum_y)
        plt.plot(self.spectrum_x, fit_value)
        plt.show()


