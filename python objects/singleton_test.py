"""
File: single_test.py
Author: Chuncheng Zhang
Date: 2025-03-06
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-03-06 ------------------------
# Requirements and constants
import time
from threading import Thread


# %% ---- 2025-03-06 ------------------------
# Function and class
class BaseClass1:
    a = 0

    def print_new_class_issue(self):
        print('New class issue: b=', self.b)

    def add_a(self):
        self.a += 1

    def loop(self):
        Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            self.add_a()
            time.sleep(0.1)
            print('Added to a=', self.a)


class NewClass1(BaseClass1):
    b = 2

    def __init__(self):
        super().__init__()
        self.a = -100

    def print_base_class_issue(self):
        print('Base class issue: a=', self.a)


# %% ---- 2025-03-06 ------------------------
# Play ground
bc1 = BaseClass1()
bc1.loop()

nc1 = NewClass1()
nc1.print_new_class_issue()
nc1.loop()

time.sleep(0.3)
nc1.print_base_class_issue()
nc1.print_new_class_issue()


# %% ---- 2025-03-06 ------------------------
# Pending


# %% ---- 2025-03-06 ------------------------
# Pending
