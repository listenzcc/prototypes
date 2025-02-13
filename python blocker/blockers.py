"""
File: blockers.py
Author: Chuncheng Zhang
Date: 2025-02-13
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Python blockers.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-02-13 ------------------------
# Requirements and constants
import time
import random
import pandas as pd
from queue import Queue
from tqdm.auto import tqdm
from IPython.display import display
from threading import Thread, RLock


# %% ---- 2025-02-13 ------------------------
# Function and class

def time_consuming_work():
    time.sleep(random.uniform(0.1, 1))
    return time.time()


t0 = time.time()
blocker_jobs = []
response_jobs = []


class Blocker1:
    '''Block by RLock.'''
    rlock = RLock()
    name = 'blocker1'

    def wait_until(self, job_id: str):
        Thread(target=self.block, args=(job_id,)).start()
        with self.rlock:
            response_jobs.append(
                dict(name=self.name, id=job_id, response=time.time()))

    def block(self, job_id: str):
        with self.rlock:
            time_consuming_work()
            blocker_jobs.append(
                dict(name=self.name, id=job_id, finished=time.time()))


class Blocker2:
    '''Block by Queue.'''
    queue: Queue = Queue(10)
    name = 'blocker2'
    timeout: float = 0.3  # seconds

    def wait_until(self, job_id: str):
        # Make sure the queue is empty.
        self.queue = Queue(10)
        Thread(target=self.block, args=(job_id,)).start()
        try:
            _ = self.queue.get(timeout=self.timeout)
            response_jobs.append(
                dict(name=self.name, id=job_id, response=time.time()))
        except:
            response_jobs.append(
                dict(name=self.name, id=job_id, response=time.time(), error='Timeout'))

    def block(self, job_id: str):
        time_consuming_work()
        self.queue.put_nowait(True)
        blocker_jobs.append(
            dict(name=self.name, id=job_id, finished=time.time()))


class Blocker3:
    '''Block by Bool flag.'''
    interval: float = 0.01
    name = 'blocker3'
    block_flag: bool = True
    timeout: float = 0.3  # seconds

    def wait_until(self, job_id: str):
        Thread(target=self.block, args=(job_id,)).start()
        t0 = time.time()
        while self.block_flag:
            time.sleep(self.interval)
            if time.time() - t0 > self.timeout:
                response_jobs.append(
                    dict(name=self.name, id=job_id, response=time.time(), error='Timeout'))
                return
        response_jobs.append(
            dict(name=self.name, id=job_id, response=time.time()))
        return

    def block(self, job_id: str):
        self.block_flag = True
        time_consuming_work()
        self.block_flag = False
        blocker_jobs.append(
            dict(name=self.name, id=job_id, finished=time.time()))

# %% ---- 2025-02-13 ------------------------
# Play ground


for i in tqdm(range(10)):
    b1 = Blocker1()
    b2 = Blocker2()
    b3 = Blocker3()
    b1.wait_until(f'{i:04d}')
    b2.wait_until(f'{i:04d}')
    b3.wait_until(f'{i:04d}')

display(blocker_jobs)
display(response_jobs)

# %%
df1 = pd.DataFrame(blocker_jobs)
df2 = pd.DataFrame(response_jobs)

table = pd.merge(df1, df2, on=['name', 'id'])
table['delay'] = table['response'] - table['finished']
table['finished'] -= t0
table['response'] -= t0
display(table)


# %% ---- 2025-02-13 ------------------------
# Pending


# %% ---- 2025-02-13 ------------------------
# Pending
