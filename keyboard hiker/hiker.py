"""
File: hiker.py
Author: Chuncheng Zhang
Date: 2024-11-15
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Hike keyboard events.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-11-15 ------------------------
# Requirements and constants
import keyboard
import argparse
from loguru import logger
from rich import print, inspect

logger.add('log/keyboard hiker.log', rotation='5 MB')

# %% ---- 2024-11-15 ------------------------
# Function and class


class KeyboardHiker(object):
    verbose = False
    suppress = False

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            logger.debug(f'Set {k} as {v}')
        logger.info('Initialized')

    def wait_until(self, key_name):
        logger.info(f'Waiting for {key_name}')
        keyboard.wait(key_name, suppress=self.suppress)
        logger.info(f'Key pressed: {key_name}')

    def bind_on_press(self):
        keyboard.on_press(self.callback, suppress=self.suppress)
        logger.debug(f'Bound with onPress event, suppress={self.suppress}')

    def callback(self, event):
        if self.verbose:
            inspect(event)
        logger.debug(f'Got key press: {event}, {event.time}')


# %% ---- 2024-11-15 ------------------------
# Play ground
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Keyboard hiker application')
    parser.add_argument('-w', '--wait-key', help='Wait for key to stop')
    parser.add_argument('-v', '--verbose', help='Verbose key press',
                        action='store_true')
    parser.add_argument('-s', '--suppress', help='Suppress the key press',
                        action='store_true',)
    namespace = parser.parse_args()
    print(namespace)

    kr = KeyboardHiker(suppress=namespace.suppress, verbose=namespace.verbose)
    kr.bind_on_press()
    kr.wait_until(namespace.wait_key)


# %% ---- 2024-11-15 ------------------------
# Pending


# %% ---- 2024-11-15 ------------------------
# Pending
