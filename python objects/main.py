"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-03-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    The main program of python objects display.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-03-04 ------------------------
# Requirements and constants
import time
from rich import print, inspect
from util import BaseObject, logger
from middleware import middleware
from multiprocessing import Process, Queue
from threading import Thread

print('Imported successfully.')

# %% ---- 2025-03-04 ------------------------
# Function and class


def run_in_thread(queue: Queue, lst: list):
    obj = BaseObject('Obj-t')
    obj.inspect()
    print(id(queue))
    for i in range(10):
        queue.put(i)
        lst.append(i)
        time.sleep(1)


def run_in_process(queue: Queue, lst: list):
    obj = BaseObject('Obj-p')
    obj.inspect()
    print(queue.qsize())
    print(len(lst))
    print(id(queue))
    for i in range(10):
        print(queue.qsize())
        print(len(lst))
        time.sleep(1)


# %% ---- 2025-03-04 ------------------------
# Play ground

if __name__ == "__main__":
    print('Logger in main', id(logger))
    queue = Queue()
    lst = []
    print(id(queue))

    obj1 = BaseObject('Obj-1')
    obj2 = BaseObject('Obj-2')

    obj1.inspect()
    obj2.inspect()

    t = Thread(target=run_in_thread, args=(queue, lst,))
    t.start()

    print('--------------------------------')
    p = Process(target=run_in_process, args=(queue, lst,))
    p.start()
    p.join()


# %% ---- 2025-03-04 ------------------------
# Pending


# %% ---- 2025-03-04 ------------------------
# Pending
