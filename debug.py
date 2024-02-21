import filewatchdog as watcher
import time

def job():
    print("I'm working...")

files = ['C:/Temp/1.txt']


watcher.once().one_of(files).modified.do(job)
watcher.once().all_of(files).modified.do(job)

watcher.once().file(f"C:\\Temp\\1.txt").modified.do(job)

watcher.once().file(f"C:\\Temp\\1.txt").exist.do(job)

watcher.once().folder("C:\Temp").modified.do(job)
watcher.once().folder("C:\Temp").exist.do(job)

while True:
    watcher.run_pending()
    time.sleep(1)