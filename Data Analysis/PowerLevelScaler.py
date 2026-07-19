# ============================================
# Power Level Scaler
# Purpose: Scale concentration values to
# reflect different power levels between
# current settings and the calibration
# settings.
# ============================================
# Imports
from datetime import datetime
from zoneinfo import ZoneInfo

import config

# File declarations
powerLog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\Power Meter\Log1.txt"
# ============================================
# Code

def getStartTime():
    with open(powerLog, 'r') as f:
        for row in f:
            if ';Logged' in row:
                line = row
                line = line.replace(';Logged:', '').strip()
                dt = datetime.strptime(line, '%d/%m/%Y at %H:%M:%S')
                dt = dt.replace(tzinfo=ZoneInfo('Asia/Tokyo'))
                return dt.timestamp()
    raise ValueError('No start time found.')

def getLatestPowerLevel(targetTime, startTime):
    latestPower = None
    latestTime = None

    with open(powerLog, 'r') as f:
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
        except Exception as e:
            print(e)
            raise ValueError('Unable to scale power level.')

        return self.powerLevel,self.scaleFactor,scaledConc, scaledErr