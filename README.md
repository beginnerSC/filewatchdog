# FileWatchdog

Runs Python functions once a certain file is created or modified. 


## Installation

.. code-block:: bash

    pip install filewatchdog


## Usage

.. code-block:: python

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
