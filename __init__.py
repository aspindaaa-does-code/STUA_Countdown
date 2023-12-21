import subprocess, multiprocessing

if __name__ in "__main__":
    multiprocessing.freeze_support()
    subprocess.Popen(["python3", "main_api.py"])
    subprocess.Popen(["python3", "main_proc.py"])
    subprocess.Popen(["python3", "main_web.py"])