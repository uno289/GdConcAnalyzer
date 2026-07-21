# ============================================
# Gadolinium Concentration Main Script
# Purpose: Call other scripts to create
#   minutely, hourly, daily analyses, graphs,
#   etc.
# NOTE: Stays running 24/7 if not aborted!
# ============================================

# Imports
import smtplib
import email.message
import datetime
import time
import config

from textwrap import dedent

# ============================================
# Alerts + Email
EMAIL = config.EMAIL
PASSWORD = config.PASSWORD

ALERTS = {
    "STP001": {
        "title": "Startup successful",
        "body": "Startup successful, all scripts working as intended."},
    "STP002": {
        "title": "Startup unsuccessful",
        "body": "Startup unsuccessful. Analyzer code not running."},
    "ANX001": {
        "title": "Large reading deviation",
        "body": "Check analysis script. Concentration changed by {}%."},
    "ANX002": {
        "title": "Erroneous reading",
        "body": "Check analysis script. Latest concentration was {}."},
    "ANX003": {
        "title": "File not processed",
        "body": "Check analysis script. Latest file ({}) was unable to be processed. File moved to Processed."},
    "ANX004": {
        "title": "Exponential fit failure",
        "body": "Check analysis script. Exponential fit failed on {}. File moved to Processed."},
    "HBX001": {
        "title": "Heartbeat failure",
        "body": "Heartbeat not detected. Check analysis script."},
    "FIM001": {
        "title": "File import length error",
        "body": "File imported was of the wrong length. Check WaveDump trace count vs. FileImport."},
    "WDP001": {
        "title": "WaveDump failure",
        "body": "Analyzer stopped. Last file was {}s ago, check WaveDump."},
    "WDP002": {
        "title": "File handling failure",
        "body": "Critical error. Last file was {}s ago, check WaveDump and FileImport."},
    "POW001": {
        "title": "Power failure",
        "body": "Power error. Last power reading was {}s ago, check StarLab."
    },
    "POW002": {
        "title": "Large scale factor deviation",
        "body": "Power error. Last timestamp/power/scale factor reading was {}, check StarLab."
    }
}

RECIPIENTS = config.EMAIL_LIST

ACTIVE_ALERTS = {}
ALERT_TIMEOUT = config.EMAIL_ALERTTIMEOUT

# ============================================
# Code
class EmailAlert:
    def __init__(self):
        pass

    def sendEmail(self,level,alert,var=None):
        now = time.time()

        if alert in ACTIVE_ALERTS:
            if now - ACTIVE_ALERTS[alert] < ALERT_TIMEOUT:
                return

        msg = email.message.EmailMessage()
        msg["Subject"] = f"[Gd Concentration Monitor] [{level}]: [{alert}] - {ALERTS[alert]['title']}"
        msg["From"] = EMAIL
        msg["To"] = ", ".join(RECIPIENTS)

        template = ALERTS[alert]["body"]

        if var is None:
            body = template
        else:
            body = template.format(var)

        msg.set_content(dedent(
        f"""
Super-K Gd Concentration Monitor Alert
        
Alert code: {alert}
Alert level: {level}

{body}

Event occurred at (JST): {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Automated message from GdConc.
"""))


        with smtplib.SMTP("smtp.gmail.com",587) as s:
            s.starttls()
            s.login(EMAIL,PASSWORD)
            s.send_message(msg)

        ACTIVE_ALERTS[alert] = now