# ============================================
# Gd Concentration Importer
# Purpose: Detect data added to pre-process
#   folder, then gather minutely datasets for
#   analysis. After analysis, move data to
#   post-process folder.
# ============================================

# Imports

import os
import csv
import shutil
import time
import DataLogging
import EventLogger
import EmailAlert
import config

# ============================================
# Code
# --------------------------------------------
mailer = EmailAlert.EmailAlert()


# Runs 1x/loop, scans config.newData for a file, and if it finds one, returns the file location/name
class scanNewFile:
    def __init__(self):
        pass
    def scanFile(self):
        files = os.listdir(config.newData)
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(config.newData, file)
                if os.path.getsize(filepath)>config.ADC_FILE_SIZE:
                    filesize1 = os.path.getsize(filepath)
                    #time.sleep(2)
                    filesize2 = os.path.getsize(filepath)
                    if filesize1!=filesize2:
                        pass
                    else:
                        return os.path.join(config.newData, file)
        return None
# --------------------------------------------

# Runs only when a file is in config.newData. After file is analyzed, deletes the file.
# Currently OVERWRITES FILES {os.remove(destination)}
class MoveFile:
    def __init__(self, fileName):
        self.fileName = fileName
    def moveFile(self):
        destination = os.path.join(config.processedData, os.path.basename(self.fileName))
        try:
            if os.path.exists(destination):
                os.remove(destination)
            if config.FILE_DELETION:
                os.remove(self.fileName)
            else:
                shutil.move(self.fileName, config.processedData)
        except PermissionError:
            message = "File still in use. Will retry next scan..."
            ErrorLog = DataLogging.errorLogger(time.time(), message)
            EventLogger.log_event("Analyzer", "WARNING", message)
# --------------------------------------------

# Runs after file is found. Creates a list with Ch1 voltages split by trace for all 600 traces. Also stores time constant for ADC.
class FileReader:
    def __init__(self, fileName):
        self.deltaTime = config.ADC_DELTATIME
        self.Ch1V = []
        self.fullList = []

    def readFile(self, fileName):
        self.filepath = fileName
        self.fileName = os.path.basename(fileName)
        with open(self.filepath, "r") as fileOne:                   # This section creates a list of the individual traces, each a list of their own
            reader = csv.reader(fileOne, delimiter='\t')
            self.unixtime = os.path.getmtime(self.filepath)         # Currently just is unix time of when the file is input - this seems to be more than enough for the data freq.

            for row_num, row in enumerate(reader):                  # Loop that adds traces to lists and appends lists to the main array
                row = [field.strip() for field in row if field.strip() != ""]
                self.deltaTime = config.ADC_DELTATIME

                try:
                    sample = int(row[0])
                except ValueError:
                    continue
                except RuntimeError:
                    EventLogger.log_event("Analyzer", "ERROR", "Trace length does not match defined length.")
                    mailer.sendEmail("ERROR","FIM001")
                if 0 <= sample <= config.ADC_SAMPLECOUNT-1:
                    self.Ch1V.append(float(row[1]))
                if sample == config.ADC_SAMPLECOUNT-1:
                    self.fullList.append(self.Ch1V.copy())
                    self.Ch1V = []
        #print("Ch1V length: ", len(self.fullList))
        return self
# --------------------------------------------

def load_waveform(fileName):                                        # Loads waveforms (used in main)
    reader = FileReader(fileName)
    reader.readFile(fileName)
    return reader
