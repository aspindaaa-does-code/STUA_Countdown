"""
Ravindra Mangar
Last Updated: 2023-12-19
Project: STUA Countdown Board

main_proc.py
----------------------------------------
This file continiously runs the export.py file, returning the data into files to be read by the main_api.py file.
In that way, the main_api.py file can be run on a different thread, and the data can be updated in real time without a delay 
caused by main_api.py running the export.py file every time a user requests data.
----------------------------------------
"""

import export
import json, multiprocessing

# Runs the export.py file, returning the data into files to be read by the main_api.py file.
def background():
    while True:

      data = json.dumps(export.export())
      with open("data.txt", "w") as g:
        g.write(data)

      lirr = json.dumps(export.export_lirr())
      with open("lirr.txt", "w") as f:
        f.write(lirr)

# Enables freezing of the multiprocessing module, to allow for multiprocessing to work on Windows.
if __name__ in "__main__":
  
    multiprocessing.freeze_support()
    background()
   