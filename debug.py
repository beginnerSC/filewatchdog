import filewatchdog as watcher
import time

def job():
    print("I'm working...")


watcher.once().folder("C:\Temp").modified.do(job)

while True:
    watcher.run_pending()
    time.sleep(1)

