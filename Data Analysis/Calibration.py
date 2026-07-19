# ============================================
# Gd Concentration Finder
# Purpose: Takes gathered |V_0| * tau value
#   and compares against line of best fit to
#   find concentration.
# ============================================
# Imports and File Definitions
import config
# --------------------------------------------

# Code
# --------------------------------------------

# This class is quite simple. The calibration is a linear equation, so we just take 3 data points, find the line of
# best fit, and place its slope under self.slope. From there, the V_0 * tau value and error are just divided by the
# slope to find our concentrations.
class Calibration:
    def __init__(self, V0_tau, Error_sqrt):
        self.slope = config.CALIBRATION_FACTOR
        self.V0_tau = V0_tau
        self.Error_sqrt = Error_sqrt
    def linearFunction(self):
        self.concentration = self.V0_tau / self.slope
        self.error = self.Error_sqrt / self.slope
        return self.concentration, self.error