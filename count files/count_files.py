"""
File: count_files.py
Author: Chuncheng Zhang
Date: 2025-03-06
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Count the files in each subdirectory.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-03-06 ------------------------
# Requirements and constants
import pandas as pd
from pathlib import Path
from rich import print

folder = Path('D:\脑机接口专项-样例库-202502')


# %% ---- 2025-03-06 ------------------------
# Function and class

result = []


def count_files_in_subdirectories(folder):
    for subfolder in folder.iterdir():
        if subfolder.is_dir():
            found = list(subfolder.rglob('*'))
            files = len([f for f in found if f.is_file()])
            folders = len([d for d in found if d.is_dir()])
            print(f"{subfolder.name}: {files} files, {folders} folders")
            result.append((subfolder.name, folders, files))


# %% ---- 2025-03-06 ------------------------
# Play ground

if __name__ == "__main__":
    count_files_in_subdirectories(folder)
    result = pd.DataFrame(result, columns=['name', 'folders', 'files'])
    print(result)


# %% ---- 2025-03-06 ------------------------
# Pending


# %% ---- 2025-03-06 ------------------------
# Pending
