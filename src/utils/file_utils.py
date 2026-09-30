import os
from pathlib import Path
from datetime import datetime

def scan_for_files(directory: Path|os.DirEntry[str]) -> list[os.DirEntry[str]]:
    """
    Recursively scans a directory for files.

    Args:
        directory (Path | DirEntry[str]): Directory to scan for files.

    Returns:
        list[DirEntry[str]]: List of DirEntry objects containing every file found.
    """
    files = []
    with os.scandir(directory) as d:
        for e in d:
            if e.is_dir():
                files.extend(scan_for_files(e))
            else:
                files.append(e)
    return files
