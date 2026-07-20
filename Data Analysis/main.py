# ============================================
# Gadolinium Concentration Main Script
# Purpose: Call other scripts to create
#   minutely, hourly, daily analyses, graphs,
#   etc.
# NOTE: Stays running 24/7 if not aborted!
# ============================================
# Imports

import config
import ModeController
import app
import threading

# ============================================
# Code
# Runs the program. Calls on everything else

def main():
    if config.ANALYZER_MODE == "Analysis":
        web_thread = threading.Thread(                      # Uses threading to start both scripts at once
            target=app.run_app,                             # Defined in app.py
            daemon=True
        )

        web_thread.start()
        ModeController.analysis_loop()

    elif config.ANALYZER_MODE == "Calibration":
        ModeController.calibration_loop()                   # No website, no startup email, writes diagnostics to CSV

if __name__ == '__main__':                                  # Necessary to run script
    main()