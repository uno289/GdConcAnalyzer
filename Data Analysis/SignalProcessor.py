# ============================================
# Gd Signal Processor
# Purpose: Zero out signals from ADC, align
#   peaks, average 600 traces into one clean
#   trace
# ============================================

# Imports

import FileImport
import numpy as np
import scipy as sp

# ============================================

# Code
# --------------------------------------------
# This class is responsible for taking in the list of 600 traces and creating one final list of 165 averaged values.
# To do so, it breaks the list of traces into individual traces, aligns all of their peaks to the same place, then
# averages all of the aligned peaks to arrive at one cleaned trace.

# NOTE: The 'listoflists' in this class arrives looking like: [[Trace 1], [Trace 2], [Trace 3], ..., [Trace 600]] and
# all traces have 165 datapoints.

class Averager:
    def __init__(self,listoflists):
        self.listoflists = listoflists
        self.averagedList = []
        self.shiftedList = []
    def align(self):                                            # Aligner function to shift all peaks to the same spot
        for pulse in self.listoflists:
            pulse = np.array(pulse)
            target = 1240                                       # The peak target - which datapoint should the peak be
            index = np.argmax(abs(pulse))
            shift = target - index                              # The amount the peak needs to be shifted by\
            #print(index)
            shifted = np.full(len(pulse), np.nan)
            if shift > 0:                                       # Moves the trace to the right
                shifted[shift:] = pulse[:-shift]
            elif shift < 0:                                     # Moves the trace to the left
                shifted[:shift] = pulse[-shift:]
            else:
                shifted = pulse
            self.shiftedList.append(np.array(shifted))          # Adds the cleaned trace to a list to average later
    def average(self):                                              # Takes the averaged list from above ^ to average

        if np.any(~np.isnan(self.shiftedList)):
            #print("Shape: ", np.shape(self.shiftedList))
            #print(self.shiftedList[:10])
            #print(self.shiftedList[-10:])
            shifted = np.array(self.shiftedList)
            all_nan_cols = np.all(np.isnan(shifted), axis=0)
            #print("Columns that are all NaN:", np.sum(all_nan_cols))
            #print("First few:", np.where(all_nan_cols)[0][:20])
            self.averagedList = np.nanmean(self.shiftedList, axis=0)    # NOTE: nanmean because the shifts add NaNs
        else:
            self.averagedList = np.nan
        return self.averagedList

# --------------------------------------------
# This class is called by main on the average of 600 traces, and examines everything prior to the peak, takes its
# median, and then subtracts that from the entire trace. This way, we zero out any net baseline voltage.

class SignalProcessor:
    def __init__(self,signal):
        self.signal = np.array(signal)
        self.start = np.argmax(abs(self.signal)) + 50                                # This 'start' is 50 points past the peak

    def zero_baseline(self):
        baseline = np.median(self.signal[:np.argmax(abs(self.signal))-300])           # This line finds the baseline
        return np.array(self.signal - baseline)                                     # This returns the adjusted code
