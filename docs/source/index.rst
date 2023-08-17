.. FileWatchdog documentation master file, created by
   sphinx-quickstart on Tue Aug 15 10:38:35 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FileWatchdog's documentation!
========================================

Runs Python functions once a certain file is created or modified. 


Installation
------------

.. code-block:: bash

   pip install filewatchdog


Usage
-----

.. code-block:: python

    import filewatchdog as watcher
    import time

    def job():
        print("I'm working...")

    files = ['C:/Temp/1.txt', 'C:/Temp/2.txt', 'C:/Temp/3.txt']

    watcher.once().one_of(files).modified.do(job)
    watcher.once().all_of(files).exist.do(job)

    def job_with_argument(name):
        print(f"I am {name}")

    watcher.once().all_of(files).exist.do(job_with_argument, name="Peter")

    while True:
        watcher.run_pending()
        time.sleep(1)
