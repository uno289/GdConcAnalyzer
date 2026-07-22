# ============================================
# Power Level Scaler
# Purpose: Scale concentration values to
# reflect different power levels between
# current settings and the calibration
# settings.
# ============================================
# Imports
import csv
from datetime import datetime
from zoneinfo import ZoneInfo

import config

# ============================================

# Code
# --------------------------------------------
# This piece runs when the main() script starts, and just grabs the start time for the power meter.
def getStartTime():
    with open(config.powerLog, 'r') as f:
        for row in f:
            if ';Logged' in row:
                line = row
                line = line.replace(';Logged:', '').strip()             # Removes the excess stuff from the start time
                dt = datetime.strptime(line, '%d/%m/%Y at %H:%M:%S')       #  Converts to time
                dt = dt.replace(tzinfo=ZoneInfo('Asia/Tokyo'))                   # Converts to Unix time in Tokyo
                return dt.timestamp()
    raise ValueError('No start time found.')

# --------------------------------------------
# The power meter only keeps local time data, so we have to grab the local time and the start time, and use those
# to find the unix time. Then we can use unix time to find the most recent prior power average for the scaling.
def getLatestPowerLevel(targetTime, startTime):
    latestPower = None
    latestTime = None

    with open(config.powerLog, 'r') as f:
        for row in f:
            try:
                relativeTime, powerLevel = row.strip().split()
                relativeTime = float(relativeTime)
                powerLevel = float(powerLevel)

                globalTime = relativeTime + startTime                   # Takes the relative time of the points and switches to unix

                if globalTime <= targetTime:                            # Only points from before the analysis time
                    if latestTime is None or globalTime > latestTime:   # Grabs the most recent point from before analysis
                        latestTime = globalTime
                        latestPower = powerLevel

                if globalTime > targetTime:
                    break

            except ValueError:
                continue

    return latestPower, latestTime                  # Tuple that gets fed into PowerLevelScaler

# --------------------------------------------
# This takes the start time, and is given the timestamp of the concentration, the concentration itself, and the error.
# It gathers the most recent power level and scales the concentration and error, returning them out and writing to
# a log for website display.

def scaleSignal(power,signal):

    scaleFactor = config.BENCHMARK_V0TAU / (config.POWER_EQN_SLOPE * power + config.POWER_EQN_OFFSET)
    scaledSignal = signal * scaleFactor
    return scaledSignal, scaleFactor

class PowerLevelScaler:
    def __init__(self):
        self.startTime = getStartTime()

    def scalePowerLevel(self, timestamp, unscaledV0Tau, unscaledError):
        self.powerLevel = getLatestPowerLevel(timestamp, self.startTime)
        if self.powerLevel[0] is None:
            raise ValueError('No power level found.')
        try:
            self.scaledSignal = scaleSignal(self.powerLevel[0], unscaledV0Tau)
            self.VCorrectedTau = self.scaledSignal[0]
            self.scaleFactor = self.scaledSignal[1]
            self.CorrectedError = unscaledError * self.scaleFactor

            with open(config.lastPowerLog, 'w') as f:               # This piece goes to the log, [timestamp, power level, scale factor]
                writer = csv.writer(f)
                writer.writerow([self.powerLevel[1],self.powerLevel[0],self.scaleFactor])

        except Exception as e:
            raise ValueError('Unable to scale power level:',e)

        return self.powerLevel,self.scaleFactor,self.VCorrectedTau,self.CorrectedError
