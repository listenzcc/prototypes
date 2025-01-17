"""
File: monitor.py
Author: Chuncheng Zhang
Date: 2024-12-13
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Server running status monitor

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-12-13 ------------------------
# Requirements and constants
import time
import curses
import _curses
import subprocess
import contextlib

from pathlib import Path
from omegaconf import OmegaConf
from loguru import logger
from threading import RLock, Thread

# Read the hosts
# Its structure is like:
# hostname:
#   host: 127.0.0.1
#   port: 8080
hosts = OmegaConf.load('./server.yaml').hosts

# %% ---- 2024-12-13 ------------------------
# Function and class


class CheckingLoop(object):
    host_name = None
    data_uptime = {}
    rlock = RLock()

    def __init__(self, host_name: str):
        self.host_name = host_name
        self.data_uptime = dict(
            host=host_name, cmd='', res='', tic=0, toc=0, status='initialized')

    def get_data(self, name):
        if name == 'uptime':
            with self.lock():
                return self.data_uptime
        return None

    @contextlib.contextmanager
    def lock(self):
        self.rlock.acquire()
        try:
            yield
        finally:
            self.rlock.release()

    def run_cmd(self, cmd='uptime'):
        v = hosts[self.host_name]
        try:
            cmd = 'ssh {} -p {} {}'.format(v['host'], v['port'], cmd)
            logger.debug(cmd)
            tic = time.time()

            # The output is in bytes, so decode it into string.
            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # print(process.communicate())
            res = b''.join(list(process.stdout.readlines()))

            # ! Why the command doesn't work in thread?
            # res = subprocess.check_output(cmd).decode('utf-8')

            status = 'success'
        except Exception as err:
            res = err
            status = 'failure'
            import traceback
            traceback.print_exc()
        finally:
            toc = time.time()
            # Update the data in the rlock
            with self.lock():
                self.data_uptime.update(dict(
                    cmd=cmd, res=res, tic=tic, toc=toc, status=status
                ))
                print(res.decode())
        return res


def get_uptime():
    output = {}
    for k, v in hosts.items():
        cmd = 'ssh {} -p {} uptime'.format(v['host'], v['port'])
        try:
            res = subprocess.check_output(cmd).decode('utf-8')
            output[k] = dict(cmd=cmd, res=res, status='success')
        except Exception as err:
            output[k] = dict(cmd=cmd, res=err, status='failure')
    return output


# %% ---- 2024-12-13 ------------------------
# Play ground
if __name__ == "__main__":
    # print(get_uptime())

    for host_name in hosts:
        cl = CheckingLoop(host_name)
        cl.run_cmd()
        cl.run_cmd('nvidia-smi')

    input('Press enter to escape.')


# %% ---- 2024-12-13 ------------------------
# Pending


# %% ---- 2024-12-13 ------------------------
# Pending
