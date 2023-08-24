import codecs
from setuptools import setup


FILEWATCHDOG_VERSION = "0.0.2"
# SCHEDULE_DOWNLOAD_URL = "https://github.com/dbader/schedule/tarball/" + SCHEDULE_VERSION


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, "r", "utf8") as f:
        return f.read()


setup(
    name="filewatchdog",
    packages=["filewatchdog"],
    version=FILEWATCHDOG_VERSION,
    description="Runs Python functions once a certain file is created or modified. ",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    license="MIT",
    author="BeginnerSC",
    # url="https://github.com/dbader/schedule",
    # download_url=SCHEDULE_DOWNLOAD_URL,
    keywords=[
        "watcher",
        "listener",
        "watchdog",
        "filewatchdog"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    install_requires=["schedule"],
)
