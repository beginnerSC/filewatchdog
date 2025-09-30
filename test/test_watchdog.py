import unittest
import os
import time
import shutil
from pathlib import Path

import filewatchdog as watcher

class TestFileWatcher(unittest.TestCase):

    TEST_DIR = "test/test_folder"
    @classmethod
    def setUpClass(cls):
        Path(cls.TEST_DIR).mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.TEST_DIR)

    def setUp(self):
        # Clear directory before each test
        for f in Path(self.TEST_DIR).glob("**/*"):
            if f.is_file():
                f.unlink()
        print("TEST_DIR exists:", os.path.isdir(self.TEST_DIR))
        print("Absolute path:", os.path.abspath(self.TEST_DIR))

    def test_new_file_detection(self):
        """Test detection of newly added file in folder"""
        triggered = []

        def on_exist():
            triggered.append("detected")

        job = watcher.once().folder(self.TEST_DIR).modified.do(on_exist)


        # Add a new file
        new_file = Path(self.TEST_DIR) / "new.txt"
        new_file.write_text("test content")

        time.sleep(1)
        watcher.run_pending()

        self.assertIn("detected", triggered)

    def test_file_modification(self):
        """Test detection of modified file"""
        triggered = []

        def on_modified():
            triggered.append("changed")

        file_path = Path(self.TEST_DIR) / "modify.txt"
        file_path.write_text("initial")

        job = watcher.once().file(str(file_path)).modified.do(on_modified)

        # Wait and modify
        time.sleep(1)
        file_path.write_text("changed content")

        time.sleep(1)
        watcher.run_pending()

        self.assertIn("changed", triggered)

    def test_ignores_deleted_files(self):
        """Test deleted file is not causing crash"""
        triggered = []

        def on_modified():
            triggered.append("triggered")

        file_path = Path(self.TEST_DIR) / "deleted.txt"
        file_path.write_text("temp")
        job = watcher.once().file(str(file_path)).modified.do(on_modified)

        file_path.unlink()  # delete file

        time.sleep(1)
        watcher.run_pending()

        self.assertNotIn("triggered", triggered)  # nothing should happen

    def test_detect_new_file_in_subfolder(self):
        """Test detection in nested subfolders"""
        triggered = []

        def on_exist():
            triggered.append("ok")

        job = watcher.once().folder(self.TEST_DIR).modified.do(on_exist)

        subfolder = Path(self.TEST_DIR) / "sub"
        subfolder.mkdir(parents=True, exist_ok=True)

        new_file = subfolder / "deep.txt"
        new_file.write_text("deep content")

        time.sleep(1)
        watcher.run_pending()

        self.assertIn("ok", triggered)


if __name__ == "__main__":
    
    print("file exists ", 
        os.path.exists("test/test_folder")
        ) 