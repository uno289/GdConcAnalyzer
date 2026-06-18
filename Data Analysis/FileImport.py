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

# --------------------------------------------
# File declarations

file0000 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC0000.CSV")
file0001 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC0001.CSV")
file1233 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1233.CSV")
file1255 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1255.CSV")
file1278 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1278.CSV")
file1283 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1283.CSV")
file1288 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1288.CSV")
file1293 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1293.CSV")
file1298 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1298.CSV")
file1303 = ("/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Old Data/WASC1303.CSV")

newData = "/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/New"                      # Input data
processedData = "/Users/keshavanand/PycharmProjects/GadoliniumAnalysis/Data/Processed"          # Dump folder after analysis

# ============================================
# Code
# --------------------------------------------

# Runs 1x/loop, scans newData for a file, and if it finds one, returns the file location/name
class scanNewFile:
    def __init__(self):
        pass
    def scanFile(self):
        files = os.listdir(newData)
        for file in files:
            if file.endswith(".txt"):
                return os.path.join(newData, file)
        return None
# --------------------------------------------

# Runs only when a file is in newData. After file is analyzed, tosses the file into processedData. Currently OVERWRITES FILES {os.remove(destination)}
class MoveFile:
    def __init__(self, fileName):
        self.fileName = fileName
    def moveFile(self):
        destination = os.path.join(processedData, os.path.basename(self.fileName))
        try:
            shutil.move(self.fileName, processedData)
        except:
            os.remove(destination)
            shutil.move(self.fileName, processedData)
# --------------------------------------------

# Runs after file is found. Creates a list with Ch1 voltages split by trace for all 600 traces. Also stores time constant for ADC.
class FileReader:
    def __init__(self, fileName):
        self.deltaTime = 4e-9
        self.Ch1V = []
        self.fullList = []

    def readFile(self, fileName):
        self.filepath = fileName
        self.fileName = os.path.basename(fileName)
        with open(self.filepath, "r") as fileOne:                   # This section creates a list of the individual traces, each a list of their own
            reader = csv.reader(fileOne, delimiter='\t')
            self.unixtime = os.path.getmtime(self.filepath)         # Currently just is unix time of when the file is input - this seems to be more than enough for the data freq.

            for row_num, row in enumerate(reader):                  # Loop that adds traces to lists and appends lists to the main array

                self.deltaTime = 4e-9

                try:
                    if 0 <= int(row[0]) <= 164:
                        self.Ch1V.append(float(row[1]))
                    if int(row[0]) == 164:
                        self.fullList.append(self.Ch1V.copy())
                        self.Ch1V = []
                except:
                    pass
        return self
# --------------------------------------------

def load_waveform(fileName):                                        # Loads waveforms (used in main)
    reader = FileReader(fileName)
    reader.readFile(fileName)
    return reader
