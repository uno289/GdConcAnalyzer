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
                line = line.replace(';Logged:', '').strip()
                dt = datetime.strptime(line, '%d/%m/%Y at %H:%M:%S')
                dt = dt.replace(tzinfo=ZoneInfo('Asia/Tokyo'))
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

                globalTime = relativeTime + startTime

                if globalTime <= targetTime:
                    if latestTime is None or globalTime > latestTime:
                        latestTime = globalTime
                        latestPower = powerLevel

                if globalTime > targetTime:
                    break

            except ValueError:
                continue

    return latestPower, latestTime                  # Tuple that gets fed into PowerLevelScaler

# --------------------------------------------
# This takes the start time, and is given the timestamp of the concentration, the concentration itself, and the error.
# It gathers the most recent power level and scales the concentration and error, returning them out.
class PowerLevelScaler:
    def __init__(self):
        self.startTime = getStartTime()

    def scalePowerLevel(self, timestamp, unscaledConc, error):
        self.powerLevel = getLatestPowerLevel(timestamp, self.startTime)
        if self.powerLevel[0] is None:
            raise ValueError('No power level found.')
        try:
            self.scaleFactor = abs(config.CALIBRATION_VOLTAGE/self.powerLevel[0])
            scaledConc = unscaledConc * self.scaleFactor
            scaledErr = error * self.scaleFactor

            with open(config.lastPowerLog, 'w') as f:
                writer = csv.writer(f)
                writer.writerow([self.powerLevel[1],self.powerLevel[0],self.scaleFactor])

        except Exception as e:
            raise ValueError('Unable to scale power level:',e)

        return self.powerLevel,self.scaleFactor,scaledConc, scaledErr