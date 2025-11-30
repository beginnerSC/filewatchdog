import schedule
import functools, datetime, logging
from pathlib import Path
from time import sleep
from typing import List, Optional, Callable
import os

logger = logging.getLogger("watcher")


class WatcherError(Exception):
    """Base watcher exception"""
    
    pass

class Watcher:
    def __init__(self) -> None:
        self.jobs: List[WatcherJob] = []

    def once(self) -> "WatcherJob":
        job = WatcherJob(self)

        return job

class WatcherJob:

    def __init__(self, watcher: Optional[Watcher] = None, check_period: int = 1, lag: int = 0, breadcrumb: str = str(Path(__file__).parent / "breadcrumb.txt")
                 ):
        """

        Check the files every `check_period` seconds to see if they exist or are modified and if so, do the job

        breadcrumb is only needed when self.event is 'exist'. The default breadcrumb path is in the same folder as this __init__.py file

        """
        self.breadcrumb: str = breadcrumb
        self.check_period: int = check_period
        self.lag: int = lag
        
        # the job job_func to run
        self.job_func: Optional[functools.partial] = None

        # list of files to watch
        self.my_folder: str = None # folder to watch
        self.files: List[str] = [] # all files to watch. remove deleted files from this list
        self.mtime_last_check: dict[str, datetime.datetime] = {} # last modified time of each file (except deleted files and new files)

        # 'exist' or 'modified'
        self.event: str = None

        # 'one_of' or 'all_of'
        self.num_of: str = None

        self.watcher: Optional[Watcher] = watcher

    @property
    def modified(self):
        self.event = 'modified'
        return self
    
    @property
    def exist(self):
        self.event = 'exist'
        return self

    @property
    def exists(self):
        self.event = 'exist'
        return self

    def file(self,file_path:str):
        """
        Watch a single file
        """
        if not Path(file_path).exists():
            print(f"Warning: The file {file_path} does not exist")
            return self
        else:
            return self.one_of([file_path])


    def __walk_folder(self, folder_path: str) -> List[str]:
        files = []
        for root, _, filenames in os.walk(folder_path):
            for file in filenames:
                files.append(os.path.join(root, file))
        return files

    def __update_files(self, files: List[str] = None):
        """
        update self.files
        """

        if files is None or len(files) == 0:
            pass
        else:
            self.files.extend(files) # add watch files to existing list
            self.files = list(set(self.files)) # remove duplicates

        delete_files = [file for file in self.files if not Path(file).exists()]
        existing_files = [file for file in self.files if file not in delete_files]
        if delete_files:
            print("The following files do not exist and are removed from watch list:", delete_files)
        self.files = existing_files

        for file in list(self.mtime_last_check.keys()):
            if file not in self.files:
                self.mtime_last_check.pop(file)

    def folder(self,folder_path:str):
        """
        Watch a folder (all files in the folder and its subfolders)
        """
        if os.path.isdir(folder_path):
            self.my_folder = folder_path
            files = self.__walk_folder(folder_path)
            return self.one_of(files)
        else:
            print(f"Folder path {folder_path} is not a directory")
            return self
            
    def one_of(self, files: List[str]): 
        """
        Watch one of the files in the list
        """
        self.num_of = 'one_of'
        self.__update_files(files)

        for file in self.files:
            if Path(file).exists():
                self.mtime_last_check.update({file: self._get_mtime(file)})
            else:
                self.files.remove(file) # remove non-existing files from watch list
        
        return self
    
    def all_of(self, files: List[str]): 
        """
            Watch all of the files in the list
        """
        self = self.one_of(files)
        self.num_of = 'all_of'
        return self

    def with_breadcrumb(self, breadcrumb: str = 'C:/Temp/breadcrumb.txt'):
        self.breadcrumb = breadcrumb
        return self
    
    def do(self, job_func: Callable, *args, **kwargs):
        self.job_func = functools.partial(job_func, *args, **kwargs)
        functools.update_wrapper(self.job_func, job_func)
        self._schedule_watcher_job()
        if self.watcher is None:
            raise WatcherError(
                "Unable to a add watcher job. "
                "Job is not associated with watcher"
            )
        self.watcher.jobs.append(self)
        return self

    def check_n_do(self):
        if self.event == 'exist':
            if ((self.num_of == 'all_of' and all([Path(file).exists() and bool(Path(file).stat().st_size) for file in self.files]))
                or (self.num_of == 'one_of' and any([Path(file).exists() and bool(Path(file).stat().st_size) for file in self.files]))):

                if not Path(self.breadcrumb).exists():
                    with open(self.breadcrumb, 'w') as f:
                        current_time = datetime.datetime.now().strftime('%H:%M')
                        f.write(f'Found everything in the watchlist at {current_time}. {self.job_func.__name__} will start in {self.lag} seconds.')

                    sleep(self.lag)
                    self.job_func()

        if self.event == 'modified':
            try:
                if self.my_folder:

                    files = self.__walk_folder(self.my_folder)
                    self.__update_files(files)
                else:
                    self.__update_files() # deleted files are removed from watch list

                
                modified_files = []
                for file in self.files:
                    try:
                        if self._was_modified(file):
                            modified_files.append(file)
                    except FileNotFoundError:
                        continue


                if (
                    (self.num_of == 'all_of' and len(modified_files) == len(self.files))
                    or (self.num_of == 'one_of' and modified_files)
                ):
                    print(f"[Watcher] Detected modification in: {modified_files}")
                    sleep(self.lag)
                    self.job_func()

            except FileNotFoundError as e:
                print(f'Watching for modification but the following files are missing: {[file for file in self.files if not Path(file).exists()]}')

    def _get_mtime(self, file: str) -> datetime.datetime:
        """returns timestamp of a file"""
        return datetime.datetime.fromtimestamp(Path(file).stat().st_mtime)

    def _was_modified(self, file: str) -> bool: 
        """`file` was modified in the past `self.check_period` seconds"""
        current_mtime = self._get_mtime(file)
        if file not in self.mtime_last_check:
            self.mtime_last_check.update({file: current_mtime})
            return True
        elif (self.mtime_last_check[file] != current_mtime):
            self.mtime_last_check.update({file: current_mtime})
            return True
        else:
            return False

    def _schedule_watcher_job(self) -> None:
        schedule.every(self.check_period).second.until(datetime.timedelta(days=10000)).do(self.check_n_do)

default_watcher = Watcher()

def once() -> WatcherJob:
    return default_watcher.once()

def run_pending() -> None:
    schedule.run_pending()
