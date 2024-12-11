"""
File: client.py
Author: Chuncheng Zhang
Date: 2024-12-02
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    TCP client implementation.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-12-02 ------------------------
# Requirements and constants
import cv2
import sys
import time
import socket
import random
import pandas as pd

from threading import Thread
from omegaconf import OmegaConf

from loguru import logger
from rich import print

config = OmegaConf.load('./config.yaml')
logger.info(f'Using config: {config}')

# %% ---- 2024-12-02 ------------------------
# Function and class


def random_bytes(n: int):
    population = 'abcdefghijklmnopqrstuvwxyz'
    random_sequence = random.choices(population=population, k=n)
    return ''.join(random_sequence).encode(config.message.encoding)


class MyClient(object):
    host = config.TCPHost.host
    port = config.TCPHost.port
    bufsize = config.TCPHost.bufsize
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.socket.connect((self.host, self.port))
        logger.info(f'Initialized {self}')

    def send_package(self, buf: bytes = None):
        if buf is None:
            n = random.randint(100, 500)
            buf = random_bytes(n)
        else:
            n = len(buf)

        head = '0x{0:0{1}X}'.format(
            n, config.message.leadingLength-2).encode(config.message.encoding)
        self.socket.send(head+buf)
        return


# %% ---- 2024-12-02 ------------------------
# Play ground
if __name__ == "__main__":
    client = MyClient()

    # Using the OpenCV video capture buf
    try:
        video = cv2.VideoCapture(0)
        fps = video.get(cv2.CAP_PROP_FPS)
        print(f'fps: {fps}')

        for _ in range(10000):
            ret, frame = video.read()
            cv2.imshow('client (src)', frame)
            cv2.pollKey()
            buf = cv2.imencode('.jpg', frame)[1].tostring()
            print(type(frame), frame.shape, type(buf), len(buf))
            client.send_package(buf)
            time.sleep(1/fps)

    finally:
        video.release()
        cv2.destroyAllWindows()

    # Using the random bytes
    # for _ in range(100):
    #     client.send_package()
    #     time.sleep(0.01)

    # Safety close the app
    sys.exit()


# %% ---- 2024-12-02 ------------------------
# Pending


# %% ---- 2024-12-02 ------------------------
# Pending
