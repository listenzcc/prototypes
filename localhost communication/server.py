"""
File: server.py
Author: Chuncheng Zhang
Date: 2024-12-02
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    TCP server implementation

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
import contextlib
import numpy as np
import pandas as pd

from threading import Thread, RLock
from omegaconf import OmegaConf

from loguru import logger
from rich import print

config = OmegaConf.load('./config.yaml')
logger.info(f'Using config: {config}')
# %% ---- 2024-12-02 ------------------------
# Function and class


class MyServer(object):
    host = config.TCPHost.host
    port = config.TCPHost.port
    bufsize = config.TCPHost.bufsize
    clients_limit = config.TCPHost.clientsLimit
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receive_buffer = []
    receive_length = 0
    rlock = RLock()

    def __init__(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.clients_limit)
        logger.info(f'Initialized {self}')

    def serve_forever(self):
        while True:
            conn, addr = self.socket.accept()
            logger.debug(f'Got connection: {conn} | {addr}')
            Thread(target=self.recv_loop(conn, addr), daemon=True).start()

    @contextlib.contextmanager
    def lock(self):
        try:
            self.rlock.acquire()
            yield
        finally:
            self.rlock.release()

    def get_buffer(self):
        if self.receive_buffer:
            with self.lock():
                return tuple(e for e in self.receive_buffer[-1])
        else:
            return

    def recv_loop(self, conn, addr):
        """
        This function continuously receives data from a connection until an empty message is received.
        The receiving process is handled in the main loop, while the returning process is handled in a separate thread for every recv.

        Parameters:
        - conn (socket.socket): The socket connection object.
        - addr (tuple): The address of the connected client.

        Returns:
        None
        """
        with self.lock():
            self.receive_buffer = []
            self.receive_length = 0
            i = 0

        while True:
            # Receive bytes from connection
            try:
                recv, t_recv = self._receive(conn)
                i += 1
            except ConnectionResetError:
                break

            # Record how many bytes were received
            with self.lock():
                self.receive_length += len(recv)
                self.receive_buffer.append((i, recv, len(recv), t_recv))

        logger.debug(f'Connection stopped: {conn} | {addr}')

        with self.lock():
            df = pd.DataFrame(
                [e[2:] for e in self.receive_buffer], columns=['length', 'time'])
        df['t2'] = df['time'] - df.loc[0, 'time']
        print(df)

        return

    def _receive(self, conn):
        # Receive header for buf remain length
        # It will also break if empty message is received
        h = conn.recv(config.message.leadingLength)
        t_recv = time.time()

        if h == b'':
            raise ConnectionResetError

        # Deal with echo package
        if h.startswith(b'0e'):
            n = int(b'0x'+h[2:], 16)
            ts = conn.recv(n)
            tsr = ts + b',' + str(t_recv).encode(config.message.encoding)
            n = len(tsr)
            head = '0e{0:0{1}X}'.format(
                n, config.message.leadingLength-2).encode(config.message.encoding)
            conn.send(head+tsr)
            logger.debug(f'Received echo packet and sent back: {ts} -> {tsr}')
            return None, t_recv

        # Deal with normal package
        try:
            body_length = int(h, 16)
        except Exception as e:
            logger.error(
                f'Received wrong number of bytes: {h}, expect like "0x12345678"')
            raise ValueError(f'Can not parse header: {h}')

        # Receive body
        array = []
        while body_length > 0:
            buf = conn.recv(min(body_length, self.bufsize))
            body_length -= len(buf)
            array.append(buf)

        # Body should be extracted but is not actually emptied.
        if body_length != 0:
            logger.error(
                f'Received unexpected number of bytes, remain_num is not ZERO: {body_length}, {array}')
            raise

        # Concatenate the array together to make recv bytes
        recv = b''.join(array)

        logger.debug(f'Received {recv[:8]} ... ({len(recv):8d}) {t_recv}')
        return recv, t_recv


# %% ---- 2024-12-02 ------------------------
# Play ground
if __name__ == '__main__':
    # Start the server
    server = MyServer()

    Thread(target=server.serve_forever, daemon=True).start()

    while True:
        if server.receive_length == 0:
            time.sleep(0.1)
            continue

        i, buf, n, t = server.get_buffer()
        nparr = np.frombuffer(buf, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print(i, n, frame.shape)
        cv2.imshow('server (dst)', frame)
        cv2.pollKey()
        # if i > 90:
        #     break
        time.sleep(1/30)

    cv2.destroyAllWindows()

    # Interacting
    while True:
        inp = input('Enter q to escape >> ')
        if inp == 'q':
            break

    # Safety close the app
    sys.exit()


# %% ---- 2024-12-02 ------------------------
# Pending


# %% ---- 2024-12-02 ------------------------
# Pending
