# ============================================
# Gadolinium Concentration Main Script
# Purpose: Call other scripts to create
#   minutely, hourly, daily analyses, graphs,
#   etc.
# ============================================
# Imports

import datetime
from random import random
import DataLogging
import time

# ============================================
# Code

# Currently just some test cases

def main():

    minutebuffer = DataLogging.oneMinuteBuffer() # takes 10Hz data and collects one minute of samples
    hourlist = DataLogging.oneHourAggregator()
    daylist = DataLogging.oneDayAggregator()

    for i in range(60000):
        timestamp = datetime.datetime.now()
        #timestamp = 100
        #concentration = 10 + random()
        concentration = 10
        datapoint = [timestamp, concentration]

        resultSecond = minutebuffer.addSample(datapoint)

        if resultSecond is not None:
            # print("One minute data set: ", resultSecond)

            minuteTotalValue = 0
            minuteAverageValue = 0

            for i in resultSecond:
                minuteTotalValue = i[1] + minuteTotalValue
                minuteAverageValue = minuteTotalValue / len(resultSecond)
            # print(minuteAverageValue)
            resultMinute = hourlist.addSample([timestamp,minuteAverageValue])





        #time.sleep(0.001)














# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

