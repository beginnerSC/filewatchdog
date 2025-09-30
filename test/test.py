

import os
import time
import filewatchdog as watcher

file_folder = "test/test_folder/"

file1 = file_folder + '1.txt'
file2 = file_folder + '2.txt'
file3 = file_folder + '3.txt'

if not os.path.isdir(file_folder):
    os.makedirs(file_folder)
for f in [file1, file2, file3]:
    if not os.path.isfile(f):
        with open(f, 'w') as fp:
            fp.write("initial content")
    else:
        print(f"File {f} already exists.")



def job():
    print("I'm working...")


# detecting changes to one single file

watcher.once().file(file1).exists.do(job)


# detecting file changes in a directory recursively

watcher.once().folder(file_folder).modified.do(job)


# watching multiple files

files = [file1, file2, file3]

watcher.once().one_of(files).modified.do(job)
watcher.once().all_of(files).exist.do(job)


while True:
    watcher.run_pending()
    time.sleep(1)