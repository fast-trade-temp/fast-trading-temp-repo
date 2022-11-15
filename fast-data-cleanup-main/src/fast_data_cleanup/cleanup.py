from genericpath import isdir
from pathlib import Path


def cleanup(dir: Path):
    if not isdir(dir):
        raise ValueError("dir should be a directory")
    for file in dir:
        file.unlink()