# ============================================
# Gd Data Logging
# Purpose: Gather data from FileImport for
#   collimating into minutely datasets. Also,
#   hold onto long-term data.
# ============================================
# Imports and File Definitions

import csv
import collections

tenMinuteData = "/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/tenMinuteData.csv"


# ============================================
# Code

# This class holds onto what comes out of FileImport at 10Hz, until 600 samples are collected.
# Once we have 600 samples, the entire dataset gets fed back to main to be smoothed.
# --------------------------------------------

class oneMinuteBuffer:
    def __init__(self):
        self.buffer = []

    def addSample(self, sample):
        self.buffer.append(sample)
        # print("Added sample: ", sample)

        if len(self.buffer) >= 600:
            minuteDataSet = self.buffer.copy()
            self.buffer.clear()
            #print("One minute dataset: ", minuteDataSet)
            #print("Buffer cleared")
            return minuteDataSet
        return None

# --------------------------------------------
# Longer-term data storage here. Data held here is [timestamp, concentration].
# Marked difference is instead of just returning data, this will hold long-term data for graphing and storage.

# There are aggregators, which just hold the data for making the data for the next level up (hourly
# collects 60 minutes, then this hourly data point sends to daily), and also a rolling cache for graphing (the
# deque(number) things).

# Every 10 minutes, one data point is kept and entered into the permanent storage CSV (DO THIS)
# --------------------------------------------

class oneHourAggregator:
    def __init__(self):
        self.oneHourData = []
        self.oneDayCache = collections.deque(maxlen=1440) # Rolling cache of 1d of minutely averages
        self.tenMinuteData = []

    def addSample(self, sample):
        self.oneHourData.append(sample)
        self.oneDayCache.append(sample)

        self.tenMinuteData.append(sample) # This one is just for keeping permanent data
        # print("Added sample: ", sample)

        if len(self.tenMinuteData) >= 10:
            tenMinuteDataSet = self.tenMinuteData.copy() # this dataset here just holds a list of 10 timestamps and concentrations
            tenMinuteMax = 0
            tenMinuteAverage = 0
            errorMax = 0
            tenMinuteError = 0

            for i in tenMinuteDataSet: # This loop is responsible for getting the average above
                tenMinuteMax = tenMinuteMax + i[1]
                tenMinuteAverage = tenMinuteMax / len(tenMinuteDataSet)
                errorMax = errorMax + i[2]
                tenMinuteError = errorMax / len(tenMinuteDataSet)

            with open(tenMinuteData, 'a', newline='') as tenMinuteDataFile: # Writing the 10m average to the permanent CSV for storage
                writer = csv.writer(tenMinuteDataFile)
                writer.writerow([tenMinuteDataSet[-1][0],tenMinuteAverage,tenMinuteError])
            self.tenMinuteData.clear()

        if len(self.oneHourData) >= 60:
            hourDataSet = self.oneHourData.copy()
            self.oneHourData.clear()
            #print("One hour dataset: ", hourDataSet)
            #print(len(hourDataSet))
            #print("Buffer cleared")
            return hourDataSet
        return None

class oneDayAggregator:
    def __init__(self):
        self.oneDayData = []
        self.oneWeekCache = collections.deque(maxlen=168) # Rolling cache of 1wk of hourly averages

    def addSample(self, sample):
        self.oneDayData.append(sample)
        self.oneWeekCache.append(sample)

        if len(self.oneDayData) >= 24:
            dayDataSet = self.oneDayData.copy()
            self.oneDayData.clear()
            return dayDataSet
        return None


class oneMonthAggregator:
    def __init__(self):
        self.oneMonthData = []
        self.oneYearCache = collections.deque(maxlen=365) #Rolling cache of 1yr of daily averages

    def addSample(self, sample):
        self.oneMonthData.append(sample)
        self.oneYearCache.append(sample)

        if len(self.oneMonthData) >= 30:
            monthDataSet = self.oneMonthData.copy()
            self.oneMonthData.clear()
            return monthDataSet
        return None



