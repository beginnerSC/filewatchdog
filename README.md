# FileWatchdog

[![Documentation Status](https://readthedocs.org/projects/filewatchdog/badge/?version=latest)](https://filewatchdog.readthedocs.io/en/latest/?badge=latest)
[![PyPI](http://img.shields.io/pypi/v/filewatchdog.svg)](https://pypi.python.org/pypi/filewatchdog/)
[![Downloads](https://static.pepy.tech/badge/filewatchdog)](https://pepy.tech/project/filewatchdog)
[![Downloads](https://static.pepy.tech/badge/filewatchdog/month)](https://pepy.tech/project/filewatchdog)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/beginnerSC/filewatchdog/blob/master/LICENSE)


Runs Python functions once a certain file is created or modified. 

## Installation

```sh
pip install filewatchdog
```

## Usage

```py
import filewatchdog as watcher
import time

def job():
    print("I'm working...")

files = ['C:/Temp/1.txt', 'C:/Temp/2.txt', 'C:/Temp/3.txt']

watcher.once().one_of(files).modified.do(job)
watcher.once().all_of(files).exist.do(job)

while True:
    watcher.run_pending()
    time.sleep(1)
```
