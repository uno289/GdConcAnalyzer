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
import config

LOCK_FILE = config.eventlog + ".lock"
lock = FileLock(LOCK_FILE)

# ============================================
# Code

def log_event(source,level,message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with lock:
        rows = []

        if os.path.exists(config.eventlog):
            with open(config.eventlog,"r",newline="",encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)

        if len(rows) == 0:
            rows.append(["Timestamp","Source","Level","Message"])

        rows.append([timestamp,source,level,message])

        if len(rows) > config.MAX_EVENTS + 1:
            rows = [rows[0]] + rows[-config.MAX_EVENTS:]

        with open(config.eventlog,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    print(f"[{level}] {source}: {message}")



