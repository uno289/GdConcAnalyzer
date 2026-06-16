# ============================================
# Gd Data Fitting
# Purpose: Take smoothed data from
#   SignalProcessor and perform exp, bi-exp,
#   log-based fits. Then find the
#   concentration from the fits
# ============================================
from importlib.resources.readers import FileReader

# Imports and File Declarations

import numpy as np
import scipy
import FileImport
import SignalProcessor
from FileImport import file0000, file0001, file1233, file1255, file1278, file1283, file1288, file1293, file1298, file1303

# ============================================
# Code

class ExponentialFit:
    def __init__(self, NPArray, deltaTime):
        self.NPArray = NPArray
        self.time_axis = deltaTime

        self.peak_index = np.argmax(np.abs(NPArray))
        self.t_peak = self.time_axis[self.peak_index]
        self.start = self.peak_index + 5

        self.x_fit = self.time_axis[self.start:]
        self.y_fit = self.NPArray[self.start:]

    def exp_fit(self, t, V_0, tau, V_BG):
        return V_0 * np.exp(-(t - self.t_peak) / tau) + V_BG

    def estimate_fit(self):
        self.x_fit = self.time_axis[self.start:]
        self.y_fit = self.NPArray[self.start:]
        p1 = [
            -0.002,  # V_0
            0.005,  # tau
            0  # V_BG
        ]
        try:
            popt, pcov = scipy.optimize.curve_fit(self.exp_fit, self.x_fit, self.y_fit, p0=p1, maxfev=10000)

            V_0, tau, V_BG = popt

            self.y_model = self.exp_fit(self.x_fit, *popt)
            print(abs(V_0 + V_BG) * tau)
            print(V_0, tau, self.t_peak, V_BG)

        except RuntimeError:
            print("Fit failed: skipping curve fit")
            popt = None
            self.y_model = None
            eq_text = "Fit failed"
