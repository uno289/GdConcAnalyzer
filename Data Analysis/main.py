# ============================================
# Gadolinium Concentration Main Script
# Purpose: Call other scripts to create
#   minutely, hourly, daily analyses, graphs,
#   etc.
# ============================================
# Imports
import numpy as np
import DataLogging
import time
import FileImport
import Grapher
import ExponentialFit
import SignalProcessor
import Calibration
from FileImport import file0000, file0001, file1233, file1255, file1278, file1283, file1288, file1293, file1298, file1303

# ============================================
# Code

# Currently just some test cases
def main():
    hourLogger = DataLogging.oneHourAggregator()  # Instantiates the hour logger

    for i in range(5):
        file = FileImport.load_waveform(file1288)                   # Imports the file
        processor = SignalProcessor.SignalProcessor(file.Ch1V)      # Loads the file into the zeroing function

        Ch1V = processor.zero_baseline()                            # Zeroes out the baseline voltage
        timeAxis = np.arange(len(file.Ch1V)) * file.deltaTime       # Time axis for the graphing function

        testrun = ExponentialFit.ExponentialFit(Ch1V, timeAxis)     # Feeds in time and voltage data for exp fit
        fit = testrun.estimate_fit()                                # Performs exp fit

        '''Graph = Grapher.Grapher(testrun, Ch1V, timeAxis)            # Graphs individual trace
        Graph.plot()'''

        calibrator = Calibration.Calibration(testrun.V0_tau)        # Loading the V_0 * tau value into the calibrator
        concentration = calibrator.linearFunction()                 # Returns concentration value
        error = 0.1 * concentration
        print("Concentration = ",round(concentration,5), "+/-", error)

        # unixtime = file.unixtime                                    # Unix timestamp of when the file was made
        unixtime = time.time()+32400
        hourLogger.addSample([unixtime, concentration, error])       # Logs the time, concentration, and error into file
        time.sleep(1)

    for i in range(5):
        file = FileImport.load_waveform(file1278)                   # Imports the file
        processor = SignalProcessor.SignalProcessor(file.Ch1V)      # Loads the file into the zeroing function

        Ch1V = processor.zero_baseline()                            # Zeroes out the baseline voltage
        timeAxis = np.arange(len(file.Ch1V)) * file.deltaTime       # Time axis for the graphing function

        testrun = ExponentialFit.ExponentialFit(Ch1V, timeAxis)     # Feeds in time and voltage data for exp fit
        fit = testrun.estimate_fit()                                # Performs exp fit

        Graph = Grapher.Grapher(testrun, Ch1V, timeAxis)            # Graphs individual trace
        Graph.plot()

        calibrator = Calibration.Calibration(testrun.V0_tau)        # Loading the V_0 * tau value into the calibrator
        concentration = calibrator.linearFunction()                 # Returns concentration value
        error = 0.1 * concentration
        print("Concentration = ",round(concentration,5), "+/-", error)

        # unixtime = file.unixtime                                    # Unix timestamp of when the file was made
        unixtime = time.time()+32400
        hourLogger.addSample([unixtime, concentration, error])       # Logs the time, concentration, and error into file
        time.sleep(1)

    for i in range(5):
        file = FileImport.load_waveform(file1233)                   # Imports the file
        processor = SignalProcessor.SignalProcessor(file.Ch1V)      # Loads the file into the zeroing function

        Ch1V = processor.zero_baseline()                            # Zeroes out the baseline voltage
        timeAxis = np.arange(len(file.Ch1V)) * file.deltaTime       # Time axis for the graphing function

        testrun = ExponentialFit.ExponentialFit(Ch1V, timeAxis)     # Feeds in time and voltage data for exp fit
        fit = testrun.estimate_fit()                                # Performs exp fit

        '''Graph = Grapher.Grapher(testrun, Ch1V, timeAxis)            # Graphs individual trace
        Graph.plot()'''

        calibrator = Calibration.Calibration(testrun.V0_tau)        # Loading the V_0 * tau value into the calibrator
        concentration = calibrator.linearFunction()                 # Returns concentration value
        error = 0.1 * concentration
        print("Concentration = ",round(concentration,5), "+/-", error)

        # unixtime = file.unixtime                                    # Unix timestamp of when the file was made
        unixtime = time.time()+32400
        hourLogger.addSample([unixtime, concentration, error])       # Logs the time, concentration, and error into file
        time.sleep(1)

    minutelyGraph = Grapher.MinutelyGraph(hourLogger.oneDayCache)
    minutelyGraph.plotLongTerm()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

