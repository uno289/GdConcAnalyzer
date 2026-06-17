# ============================================
# Gd Concentration Finder
# Purpose: Takes gathered |V_0| * tau value
#   and compares against line of best fit to
#   find concentration.
# ============================================
# Imports and File Definitions
# --------------------------------------------
# Code

class Calibration:
    def __init__(self, V0_tau):
        self.slope = 0.000113781 # THIS ONLY WORKS FOR 1233, 1278, 1288!!!
        # self.slope = 0.00020634 # THIS ONLY WORKS FOR 1255, 1283, 1293!!!
        self.V0_tau = V0_tau
    def linearFunction(self):
        concentration = self.V0_tau / self.slope
        return concentration