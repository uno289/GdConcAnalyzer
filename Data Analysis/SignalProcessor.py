# ============================================
# Gd Processor
# Purpose: Smooth signals from ADC, normalize
#   data as needed
# ============================================

# Imports

import FileImport
import numpy as np
import scipy as sp
from FileImport import file0000, file0001, file1233, file1255, file1278, file1283, file1288, file1293, file1298, file1303

# ============================================

# Code
# --------------------------------------------
# Test zero

class SignalProcessor:
    def __init__(self,signal):
        self.signal = np.array(signal)
        self.start = np.argmax(abs(self.signal)) + 5

    def zero_baseline(self):
        self.start = np.argmax(abs(self.signal)) + 5
        baseline = np.median(self.signal[:np.argmax(abs(self.signal))-3])
        return np.array(self.signal - baseline)



# --------------------------------------------