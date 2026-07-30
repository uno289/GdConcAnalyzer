import csv
import os
import time
from zoneinfo import ZoneInfo

import pandas
import numpy
from datetime import datetime


file = r"D:\20260729Data\Waveforms\Acq_dig1-DT5724-148_20260728142130-05.txt"
powerlog = r"D:\20260729Data\Log1.txt"

def grabFileLogs():

    first_timestamp = None
    final_timestamp = 0
    clock_period = 10

    with open(file) as f:
        creation_time = int(os.path.getctime(file) * 1e9)
        reader = csv.reader(f)
        for row in reader:
            if "TimeStamp" in row[0]:
                timestripped = int(row[0].split(":")[1])

                if first_timestamp is None:
                    first_timestamp = timestripped

                relative_time = timestripped - first_timestamp
                timecorrected = creation_time + (relative_time*clock_period)
                final_timestamp = timecorrected/1e9
            else:
                continue
    print("Final timestamp: ", final_timestamp)
    return final_timestamp

# This piece runs when the main() script starts, and just grabs the start time for the power meter.
def getStartTime():
    with open(powerlog, 'r') as f:
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

    with open(powerlog, 'r') as f:
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
    print("Latest power level: ", latestPower)
    print("Latest power time: ", latestTime)

getLatestPowerLevel(grabFileLogs(),getStartTime())
