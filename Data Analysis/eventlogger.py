# ============================================
# Event Logger
# Purpose: Rolling log of most recent events
#   done by main() and app().
# ============================================
# Imports
import csv
import os
import datetime
import time
from filelock import FileLock
import main

eventlog = r"C:\Users\water\Desktop\GadoliniumAnalysis\Data\eventlogger.csv"
LOCK_FILE = eventlog + ".lock"
lock = FileLock(LOCK_FILE)

# ============================================
# Code

def log_event(source,level,message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with lock:
        rows = []

        if os.path.exists(eventlog):
            with open(eventlog,"r",newline="",encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)

        if len(rows) == 0:
            rows.append(["Timestamp","Source","Level","Message"])

        rows.append([timestamp,source,level,message])

        if len(rows) > main.max_events + 1:
            rows = [rows[0]] + rows[-main.max_events:]

        with open(eventlog,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    print(f"[{level}] {source}: {message}")



