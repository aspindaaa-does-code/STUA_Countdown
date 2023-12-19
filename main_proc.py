import export
import json, multiprocessing

def background():
    while True:

      data = json.dumps(export.export())
      with open("data.txt", "w") as g:
        g.write(data)

      lirr = json.dumps(export.export_lirr())
      with open("lirr.txt", "w") as f:
        f.write(lirr)

if __name__ in "__main__":
  
    multiprocessing.freeze_support()
    background()
   