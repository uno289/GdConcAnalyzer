# ============================================
# Gadolinium Concentration Main Script
# Purpose: Call other scripts to create
#   minutely, hourly, daily analyses, graphs,
#   etc.
# NOTE: Stays running 24/7 if not aborted!
# ============================================
# Imports
import numpy as np
import time

import DataLogging
import Grapher
import ExponentialFit
import SignalProcessor
import Calibration
import FileImport
from FileImport import file0000, file0001, file1233, file1255, file1278, file1283, file1288, file1293, file1298, file1303

# ============================================
# Code

# Currently just some test cases
def main():
    hourLogger = DataLogging.oneHourAggregator()                        # Instantiates the hour logger

    while True:                                                         # Loop keeps the program running forever
        scanner = FileImport.scanNewFile()                              # Continuously scans for a new file
        file_path = scanner.scanFile()                                  # If a file exists, this locates it

        if file_path is not None:
            print("File found. Analyzing...")
            file = FileImport.load_waveform(file_path)                  # Imports the file
            listoflists = file.fullList                                 # All 600 runs, each one is 165 samples

            avg = SignalProcessor.Averager(listoflists)
            avg.align()
            Ch1V = avg.average()

            processor = SignalProcessor.SignalProcessor(Ch1V)           # Loads the file into the zeroing function

            Ch1VZeroed = processor.zero_baseline()                      # Zeroes out the baseline voltage
            timeAxis = np.arange(len(Ch1VZeroed)) * file.deltaTime      # Time axis for the graphing function

            testrun = ExponentialFit.ExponentialFit(Ch1VZeroed, timeAxis)     # Feeds in time and voltage data for exp fit
            fit = testrun.estimate_fit()                                # Performs exp fit

            Graph = Grapher.Grapher(testrun, Ch1VZeroed, timeAxis)            # Graphs individual trace
            Graph.plot()


            calibrator = Calibration.Calibration(testrun.V0_tau,testrun.Error_sqrt)              # Loading the V_0 * tau value into the calibrator

            concentration = calibrator.linearFunction()                 # Returns concentration value AND error
            error = 0.1 * concentration[0] + concentration[1]           # Systematic error = 10%, adding the uncertainty

            # unixtime = file.unixtime                                    # Unix timestamp of when the file was made
            unixtime = time.time()+32400                                # Shifts time zone to Japan time (TEMP)
            hourLogger.addSample([unixtime, concentration[0], error])   # Logs the time, concentration, and error into file

            fileMover = FileImport.MoveFile(file_path)                  # Loads the file mover (post-processing)
            fileMover.moveFile()                                        # Moves the processed file out
            # time.sleep(1)

            LongTermGraph = Grapher.MinutelyGraph(hourLogger.oneDayCache)   # Loads the minutely grapher
            LongTermGraph.plotLongTerm()                                # Graphs the minutely concentration for the past day

        print("Loop successful. Sleeping for 5 seconds...")
        time.sleep(5)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':                                              # Necessary to run script
    main()