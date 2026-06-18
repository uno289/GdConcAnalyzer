# ============================================
# Gd Data Fitting
# Purpose: Take smoothed data from
#   SignalProcessor and perform exp, bi-exp,
#   log-based fits. Then find the
#   concentration from the fits
# ============================================

# Imports and File Declarations

import numpy as np
import scipy
# ============================================

# Code
# --------------------------------------------

# This class tries to do an exponential fit on the data that SignalProcessor has zeroed. If it fails, then an error is
# printed to show the failure.
class ExponentialFit:
    def __init__(self, NPArray, deltaTime):                     # This section instantiates all the data for the fit
        self.NPArray = NPArray                                  # Data shows up as a numpy array
        self.time_axis = deltaTime                              # delta T for the measurement

        self.peak_index = np.argmax(np.abs(NPArray))            # Where's the peak, self.start goes 5 points past it
        self.t_peak = self.time_axis[self.peak_index]
        self.start = self.peak_index + 2

        self.x_fit = self.time_axis[self.start:]                # Tells the fit what the x and y parameters are
        self.y_fit = self.NPArray[self.start:]

    def exp_fit(self, t, V_0, tau, V_BG):                       # IMPORTANT: This is the fit function!
        return V_0 * np.exp(-(t - self.t_peak) / tau) + V_BG

    def estimate_fit(self):
        self.x_fit = self.time_axis[self.start:]
        self.y_fit = self.NPArray[self.start:]
        p1 = [
            -0.002,  # V_0
            0.005,   # tau
            0        # V_BG
        ]
        # This section is where the fit is attempted. scipy tries to fit the curve, forcing tau positive, and if it
        # fails it skips past. If it succeeds, it outputs V_0 * tau (area under the curve) for calibrating for Gd conc.
        try:
            popt, pcov = scipy.optimize.curve_fit(self.exp_fit, self.x_fit, self.y_fit, p0=p1,bounds=([-np.inf, 0, -np.inf],[np.inf, np.inf, np.inf]), maxfev=10000)
            V_0, tau, V_BG = popt
            self.y_model = self.exp_fit(self.x_fit, *popt)
            # print("V0 Tau: ", abs(V_0 + V_BG) * tau)
            self.V0_tau = abs(V_0 + V_BG) * tau

            # Error correction below:
            A = V_0 + V_BG
            self.V_0 = V_0
            self.tau = tau
            self.V_BG = V_BG

            # This section is responsible for calculating covariance errors. Matrix multiplication with J, J transpose
            # around the covariance matrix pcov.
            J = np.array([tau, A, tau])

            self.Error_var = J @ pcov @ J.T
            self.Error_sqrt = np.sqrt(self.Error_var)
            # print("Error_sqrt: ", self.Error_sqrt)

        except RuntimeError:
            print("Fit failed: skipping curve fit")
            popt = None
            self.y_model = None
            eq_text = "Fit failed"
