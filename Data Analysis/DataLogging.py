# ============================================
# Gd Data Logging
# Purpose: Gather data from FileImport for
#   collimating into minutely datasets. Also,
#   hold onto long-term data.
# ============================================
# Imports and File Definitions

import csv
import collections

oneMinuteFile = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\oneMinuteData.csv"
tenMinuteFile = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\tenMinuteData.csv"
HourlyFile = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\hourlyData.csv"
DailyFile = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\dailyData.csv"
errorLog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\errorLog.csv"

# ============================================
# Code

# Longer-term data storage here. Data held here is [timestamp, concentration, error].
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
        self.hourDataSet = []

    def __len__(self):
        return len(self.oneHourData)

    def addSample(self, sample):
        self.oneHourData.append(sample)
        self.oneDayCache.append(sample)

        self.tenMinuteData.append(sample) # This one is just for keeping permanent data
        # print("Added sample: ", sample)
        with open(oneMinuteFile, 'a', newline='') as oneMinuteDataFile:
            writer = csv.writer(oneMinuteDataFile)
            writer.writerow(sample)

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

            with open(tenMinuteFile, 'a', newline='') as tenMinuteDataFile: # Writing the 10m average to the permanent CSV for storage
                writer = csv.writer(tenMinuteDataFile)
                writer.writerow([tenMinuteDataSet[-1][0],tenMinuteAverage,tenMinuteError])
            self.tenMinuteData.clear()

        if len(self.oneHourData) >= 60:
            self.hourDataSet = self.oneHourData.copy()
        return None

class oneDayAggregator:
    def __init__(self):
        self.oneDayData = []
        self.oneWeekCache = collections.deque(maxlen=168) # Rolling cache of 1wk of hourly averages

    def __len__(self):
        return len(self.oneDayData)

    def addSample(self, sample):
        self.oneDayData.append(sample)
        self.oneWeekCache.append(sample)
        with open(HourlyFile, 'a', newline='') as hourlyDataFile:
            writer = csv.writer(hourlyDataFile)
            writer.writerow(sample)

        if len(self.oneDayData) >= 24:
            dayDataSet = self.oneDayData.copy()
            return dayDataSet
        return None


class oneMonthAggregator:
    def __init__(self):
        self.oneMonthData = []
        self.oneYearCache = collections.deque(maxlen=365) #Rolling cache of 1yr of daily averages

    def __len__(self):
        return len(self.oneMonthData)

    def addSample(self, sample):
        self.oneMonthData.append(sample)
        self.oneYearCache.append(sample)

        with open(DailyFile, 'a', newline='') as dailyDataFile:
            writer = csv.writer(dailyDataFile)
            writer.writerow(sample)

        if len(self.oneMonthData) >= 30:
            monthDataSet = self.oneMonthData.copy()
            return monthDataSet
        return None

class errorLogger:
    def __init__(self, errorTime, errorLog):
        self.errorLogData = [errorTime, errorLog]
    def errorLogging(self, ):
        with open(errorLog, 'a', newline='') as errorLogFile:
            writer = csv.writer(errorLogFile)
            writer.writerow([self.errorLogData[0], self.errorLogData[1]])
