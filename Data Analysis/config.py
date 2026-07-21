# ============================================
# GdConc Config
# Purpose: Holds all configurable settings
# and email instructions in one file.
# ============================================
# Imports

import EmailandPass

# ============================================
# Code

# main.py
ANALYZER_MODE = "Analysis"       # Choose between "Analysis" or "Calibration" to swap modes

# --------------------------------------------
# EmailAlert.py

EMAIL = EmailandPass.EMAIL          # Hidden for password protection
PASSWORD = EmailandPass.PASSWORD    # Hidden for password protection
EMAIL_ALERTTIMEOUT = 3600           # 1hr lock on repeat error emails
EMAIL_LIST = [
    "katrumpeter@gmail.com",
    "kanand289@gmail.com"
]

# --------------------------------------------
# FileImport.py
FILE_DELETION = True            # Turns on/off file deletion
ADC_FILE_SIZE = 20000           # File size when completed in bytes
ADC_DELTATIME = 1.28e-6         # Time between samples in seconds
ADC_SAMPLECOUNT = 7813          # How many samples per trace

# --------------------------------------------
# Calibration.py
CALIBRATION_FACTOR = 0.293811   # Adjusts slope of calibration

# --------------------------------------------
# Grapher.py
TRACE_COUNT = 200               # Replace with current trace count per minute

# --------------------------------------------
# EventLogger.py
MAX_EVENTS = 15                 # Rolling log amount for the event logger

# --------------------------------------------
# SignalProcessor.py
PEAK_TARGET = 1002              # Tells SignalProcessor roughly where the peak is

# --------------------------------------------
# PowerLevelScaler.py
CALIBRATION_VOLTAGE = 0.000295   # This value is in W, whatever calibration voltage was used
POWER_SCALE_MIN = 0.4          # Used by app.py to check power scaling factor
POWER_SCALE_MAX = 1.5           # Used by app.py to check power scaling factor

# --------------------------------------------
# app.py
USE_WAITRESS = True             # Toggles the website production environment
WEBPROD = True                  # Tells the website to use dedicated ip

# ============================================
# File declarations

# --------------------------------------------
# Heartbeats/Startup Stats
startup = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\startup.csv"                         # Startup time
runs = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\runcount.csv"                           # Runs since startup
heartbeat = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Heartbeat.csv"                     # main.py heartbeat
wavedumpcheck = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\wavedumpHB.csv"                # WaveDump file heartbeat

# --------------------------------------------
# Logs
eventlog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\eventlogger.csv"                    # Rolling event log
powerLog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Power Meter\Log1.txt"               # Power meter log
errorLog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\errorLog.csv"                       # Permanent error log
lastPowerLog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\lastPowerLog.csv"               # Last power reading log

# --------------------------------------------
# Data
singleTrace = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Results\current_trace.html"      # HTML of one averaged trace
oneMinuteCSV = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\oneMinuteData.csv"              # Minutely data, forever
oneHourCSV = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\hourlyData.csv"                   # Hourly data, forever
oneDayCSV = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\dailyData.csv"                     # Daily data, forever

calibrationCSV = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\calbrationCSV.csv"            # Only used in calibration, data compiler

# --------------------------------------------
# Data folders
newData = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\New"                                 # Input data
processedData = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Processed"                     # Dump folder after analysis