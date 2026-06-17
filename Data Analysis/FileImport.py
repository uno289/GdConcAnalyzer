# ============================================
# Gd Concentration Importer
# Purpose: Import data from oscilloscope, then
#   gather minutely datasets for analysis.
# ============================================

# Imports

import os
import csv
import numpy as np
import scipy as sp
import pandas as pd

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


# ============================================
# Code

class FileReader:
    def __init__(self, fileName):
        self.deltaTime = 0
        self.Ch1V = []
        self.Ch4V = []

    def readFile(self, fileName):
        self.filepath = fileName
        self.fileName = os.path.basename(fileName)
        with open(self.filepath, "r") as fileOne:
            reader = csv.reader(fileOne)
            self.unixtime = os.path.getmtime(self.filepath)

            for row_num, row in enumerate(reader, start=1):

                if row[0] == "Delta(second)":
                    self.deltaTime = float(row[1])

                if row_num < 31:
                    continue

                if row[0] != '':
                    self.Ch1V.append(float(row[0]))
                if row[3] != '':
                    self.Ch4V.append(float(row[3]))
        print(self.filepath)
        return self

def load_waveform(fileName):
    reader = FileReader(fileName)
    reader.readFile(fileName)
    return reader
