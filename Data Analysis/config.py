# ============================================
# GdConc Config
# Purpose: Holds all configurable settings
# and email instructions in one file.
# ============================================
# Imports

import EmailandPass

# Code

# --------------------------------------------
# main.py


# --------------------------------------------
# EmailAlert.py

EMAIL = EmailandPass.EMAIL          # Hidden for password protection
PASSWORD = EmailandPass.PASSWORD    # Hidden for password protection
EMAIL_LIST = [
    "katrumpeter@gmail.com",
    "kanand289@gmail.com"
]

# --------------------------------------------
# FileImport.py
FILE_DELETION = True            # Turns on/off file deletion
ADC_FILE_SIZE = 4450000         # File size when completed in bytes
ADC_DELTATIME = 1.28e-6         # Time between samples in seconds
ADC_SAMPLECOUNT = 7814          # How many samples per trace

# --------------------------------------------
# Calibration.py
CALIBRATION_FACTOR = 0.293811   # Adjusts slope of calibration

# --------------------------------------------
# EmailAlert.py
EMAIL_ALERTTIMEOUT = 3600       # 1hr

# --------------------------------------------
# eventlogger.py
MAX_EVENTS = 15                 # Rolling log amount for the event logger

# --------------------------------------------
# SignalProcessor.py
PEAK_TARGET = 1240              # Tells SignalProcessor roughly where the peak is

# --------------------------------------------
# PowerLevelScaler.py
CALIBRATION_VOLTAGE = 0.295     # This value is in mW

# --------------------------------------------
# app.py
USE_WAITRESS = True             # Toggles the website production environment
WEBPROD = True                  # Tells the website to use dedicated app