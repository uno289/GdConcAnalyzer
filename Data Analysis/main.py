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
import csv
import collections

import DataLogging
import Grapher
import ExponentialFit
import SignalProcessor
import Calibration
import FileImport
import eventlogger
import EmailAlert
import PowerLevelScaler
import config

# File declarations
heartbeat = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Heartbeat.csv"
wavedumpcheck = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\wavedumpHB.csv"
eventlog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\eventLog.csv"
startup = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\startup.csv"
runs = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\runcount.csv"
# ============================================
# Code
# Runs the program. Calls on everything else
def main():
    mailer = EmailAlert.EmailAlert()
    eventlogger.log_event("Analyzer","INFO","[STP001] Process started.")    # Logs to webpage

    mailer.sendEmail("INFO","STP001")                        # Sends startup email

    with open(startup, "w") as f:
        f.write(str(time.time()))                                       # Used to keep track of startup/uptime

    with open(runs, "w") as f:                                          # Resets the run counter
        f.write(str(0))

    hourLogger = DataLogging.oneHourAggregator()                        # Instantiates the hour logger
    dayLogger = DataLogging.oneDayAggregator()                          # Instantiates the day cache
    yearLogger = DataLogging.oneMonthAggregator()                       # Instantiates the year cache

    MinuteCSV = DataLogging.oneMinuteFile
    HourCSV = DataLogging.HourlyFile
    DayCSV = DataLogging.DailyFile

    pscaler = PowerLevelScaler.PowerLevelScaler()                       # Finds power logger start time

    try:
        with open(MinuteCSV,'r', newline = '') as r:
            newest_rows = collections.deque(csv.reader(r),maxlen=1440)
            for i,row in enumerate(newest_rows):
                #print(f"{i}: {repr(row)} (len={len(row)})")
                if i > 0:
                    #print(row[0],row[1],row[2])
                    hourLogger.oneDayCache.append([float(row[0]), float(row[1]), float(row[2])])    # Fills the minutely cache with 1 day's worth of data

    except Exception as e:
        print("Error: ",e)
        eventlogger.log_event("Analyzer","INFO","[STP002] Empty minute cache. Instantiating minute graph with no data.")

    try:
        with open(HourCSV,'r', newline = '') as r:
            newest_rows = collections.deque(csv.reader(r),maxlen=168)
            for i, row in enumerate(newest_rows):
                if i > 0:
                    dayLogger.oneWeekCache.append([row[0], row[1], row[2]])                         # Fills hourly cache with 1 week of data
    except:
        eventlogger.log_event("Analyzer","INFO","[STP002] Empty hour cache. Instantiating hour graph with no data.")

    try:
        with open(DayCSV,'r', newline = '') as r:
            newest_rows = collections.deque(csv.reader(r),maxlen=365)
            for i,row in enumerate(newest_rows):
                if i>0:
                    yearLogger.oneYearCache.append([row[0], row[1], row[2]])                        # Fills daily cache with 1 year of data
    except:
        eventlogger.log_event("Analyzer","INFO","[STP002] Empty day cache. Instantiating day graph with no data.")


    while True:                                                         # Loop keeps the program running forever
        scanner = FileImport.scanNewFile()                              # Continuously scans for a new file
        file_path = scanner.scanFile()                                  # If a file exists, this locates it

        if file_path is not None:
            eventlogger.log_event("Analyzer","INFO","File found. Analyzing...")
            try:
                file = FileImport.load_waveform(file_path)                  # Imports the file
                listoflists = file.fullList                                 # All 600 runs, each one is 165 samples
                #print("Checkpoint1:", len(listoflists))
                with open(wavedumpcheck, "w") as f:
                    f.write(str(time.time()))                               # Writes to wavedump heartbeat

                avg = SignalProcessor.Averager(listoflists)                 # Loads files into averager
                avg.align()                                                 # Aligns all samples to same peak
                Ch1V = avg.average()                                        # Averages all samples to one curve
                #print("Checkpoint2:", len(Ch1V))
                processor = SignalProcessor.SignalProcessor(Ch1V)           # Loads the file into the zeroing function

                Ch1VZeroed = processor.zero_baseline()                      # Zeroes out the baseline voltage
                timeAxis = np.arange(len(Ch1VZeroed)) * file.deltaTime      # Time axis for the graphing function

                testrun = ExponentialFit.ExponentialFit(Ch1VZeroed, timeAxis)     # Feeds in time and voltage data for exp fit
                fit = testrun.estimate_fit()                                      # Performs exp fit

                Graph = Grapher.Grapher(testrun, Ch1VZeroed, timeAxis)            # Graphs individual trace
                Graph.plot()

                calibrator = Calibration.Calibration(testrun.V0_tau,testrun.Error_sqrt)  # Loading the V_0 * tau value into the calibrator

                concentration = calibrator.linearFunction()                        # Returns concentration value AND error
                error = round(0.1 * concentration[0] + concentration[1],5)         # Systematic error = 10%, adding the uncertainty
                # print("Concentration: ", round(concentration[0],5), ", Error: ", error)

                unixtime = time.time()+32400                                # Shifts time zone to Japan time (TEMP)

                scaledVals = pscaler.scalePowerLevel(unixtime,concentration[0], error)
                print(scaledVals)

                hourLogger.addSample([unixtime, round(concentration[0],5), error])   # Logs the time, concentration, and error into file

                fileMover = FileImport.MoveFile(file_path)                  # Loads the file mover (post-processing)
                fileMover.moveFile()                                        # Moves the processed file out
                # time.sleep(1)

                try:
                    if len(hourLogger.oneHourData) >= 60:
                        eventlogger.log_event("Analyzer","INFO","Hourly graph updated with most recent average.")
                        houravg = np.average([s[1] for s in hourLogger.oneHourData])
                        hourerror = np.average([s[2] for s in hourLogger.oneHourData])
                        hourtime = time.time() + 32400
                        dayLogger.addSample([hourtime, houravg, hourerror])                     # If there is 1 hour of data, this runs to add an hourly average
                        hourLogger.oneHourData.clear()

                except RuntimeError:
                    eventlogger.log_event("Analyzer","ERROR","Error encountered when adjusting hourly average!")
                    pass

                try:
                    if len(dayLogger.oneDayData) >= 24:
                        eventlogger.log_event("Analyzer","INFO","Daily graph updated with most recent average.")
                        dayavg = np.average([s[1] for s in dayLogger.oneDayData])
                        hourerror = np.average([s[2] for s in dayLogger.oneDayData])
                        daytime = time.time() + 32400
                        yearLogger.addSample([daytime, dayavg, hourerror])                      # If there is one day of data, this runs to add a daily average
                        dayLogger.oneDayData.clear()

                except RuntimeError:
                    eventlogger.log_event("Analyzer", "ERROR", "Error encountered when adjusting daily average!")
                    pass


                MinutelyOneDayGraph = Grapher.MinutelyGraph(hourLogger.oneDayCache)   # Loads the minutely grapher
                MinutelyOneDayGraph.plotMinutely()                                    # Graphs the minutely concentration for the past day

                HourlyOneWeekGraph = Grapher.HourlyGraph(dayLogger.oneWeekCache)      # Loads the hourly grapher
                HourlyOneWeekGraph.plotHourly()                                       # Graphs the average hourly concentration for past week

                DailyOneYearGraph = Grapher.DailyGraph(yearLogger.oneYearCache)       # Loads the daily grapher
                DailyOneYearGraph.plotDaily()                                         # Graphs the average daily concentration for past year

                eventlogger.log_event("Analyzer","INFO","Loop successful. Sleeping for 30 seconds...")

            except Exception as e:
                eventlogger.log_event("Analyzer","ERROR","RuntimeError encountered. Sleeping for 30 seconds...")
                mailer.sendEmail("ERROR","ANX003","placeholder")
                unixtime = time.time()
                log = DataLogging.errorLogger(unixtime, e)                          # Logs when things break due to Python
                log.errorLogging()

                fileMover = FileImport.MoveFile(file_path)                          # Loads the file mover (post-processing)
                fileMover.moveFile()
        else:
            pass
            eventlogger.log_event("Analyzer","INFO","No file. Sleeping for 30 seconds...")

        with open(heartbeat,"w") as f:
            f.write(str(time.time()))                          # Writes heartbeats to the webpage

        with open(runs,"r+") as f:
            runcount = int(f.read())
            f.seek(0)
            f.write(str(runcount+1))                           # Run counter
            f.truncate()

            time.sleep(30)                                     # Time in seconds between each pass (set to 1/2 reception time)

if __name__ == '__main__':                                  # Necessary to run script
    main()