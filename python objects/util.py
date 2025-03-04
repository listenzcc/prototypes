"""
File: util.py
Author: Chuncheng Zhang
Date: 2025-03-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Class library.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-03-04 ------------------------
# Requirements and constants
from loguru import logger
from rich import print


# %% ---- 2025-03-04 ------------------------
# Function and class

class BaseObject:
    public_array = []
    private_array = None
    name = ''

    def __init__(self, name: str = 'Base object'):
        self.private_array = []
        self.name = name

    def inspect(self):
        print(self.name)
        print('>>', id(self))
        print('>>', '1 |', id(self.public_array))
        print('>>', '2 |', id(self.private_array))
        pass


# %% ---- 2025-03-04 ------------------------
# Play ground


# %% ---- 2025-03-04 ------------------------
# Pending


# %% ---- 2025-03-04 ------------------------
# Pending
