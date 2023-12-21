"""
Ravindra Mangar
Last Updated: 2023-12-19
Project: STUA Countdown Board

__init__.py
----------------------------------------
This files runs the API, the web app, and the main program, all at once.
To properly terminate this program, type anything into the console and press enter.
----------------------------------------
"""

# Imports
import subprocess, multiprocessing


if __name__ in "__main__":
    multiprocessing.freeze_support() # Enables freezing of the multiprocessing module, to allow for multiprocessing to work on Windows.
    
    # Runs the STUA Countdown Board API, web app, and main program.
    main_api = subprocess.Popen(["python3", "main_api.py"])
    main_proc = subprocess.Popen(["python3", "main_proc.py"])
    main_web = subprocess.Popen(["python3", "main_web.py"])

    # Allows for the program to be terminated by typing anything into the console and pressing enter.
    while True:
        if input():
            # Terminates the API, web app, and main program.
            main_api.kill()
            main_proc.kill()
            main_web.kill()
            break