"""
File: screen.py
Author: Chuncheng Zhang
Date: 2024-11-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Screen for curses demo.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-11-18 ------------------------
# Requirements and constants
import sys
import time
import curses
import _curses
import keyboard
import datetime
import subprocess
import numpy as np

from threading import Thread
from rich import print
from curses import wrapper
from wcwidth import wcswidth
from curses.textpad import Textbox, rectangle

import locale
locale.setlocale(locale.LC_ALL, '')
pref_encoding = locale.getpreferredencoding()

# %% ---- 2024-11-18 ------------------------
# Function and class
# cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description, MainWindowTitle'
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# for line in proc.stdout:
#     if line.rstrip():
#         # only print lines that are not empty
#         # decode() is necessary to get rid of the binary string (b')
#         # rstrip() to remove `\r\n`
#         print(line.decode('gbk').rstrip())


def main_deprecated(stdscr: _curses.window):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(11):
        v = i+1
        stdscr.addstr(i, 0, 20 * f'10 divided by {v} is {10 / v}')

    # for _ in range(5):
    #     stdscr.echochar(stdscr.getkey())

    # curses.echo()
    stdscr.box()

    # print(stdscr.getkey())
    # print(stdscr.get_wch())
    s = stdscr.getstr()
    print(s)
    stdscr.refresh()

    stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
    stdscr.addstr(1, 0, s)

    editwin = curses.newwin(5, 30, 3, 1)
    # rectangle(stdscr, 1, 0, 1+5+1, 1+30)
    stdscr.refresh()

    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()
    print(message)
    # print(stdscr.getkey())

    return 0


class TimeConverter(object):
    fmt: str = '%Y-%m-%d %H:%M:%S.%f'
    t0: float = None
    t: float = None
    s: str = None

    def __init__(self):
        self.tick()

    def tick(self):
        t = time.time()
        self.string_to_timestamp(self.timestamp_to_string(t))
        self.t0 = t
        return t

    def string_to_timestamp(self, s: str) -> float:
        t = datetime.datetime.strptime(s, self.fmt).timestamp()
        self.t = t
        return t

    def timestamp_to_string(self, t: float) -> str:
        dt = datetime.datetime.fromtimestamp(t)
        s = dt.strftime(self.fmt)
        self.s = s
        return s


tc = TimeConverter()
print(f't0: {tc.t0}')
print(f's: {tc.s}')
print(f't: {tc.t}')


class CursesPad(object):
    nlines: int = 8
    ncols: int = 80
    y: int = 0
    x: int = 0
    name: str = 'Pad-?'
    pad: _curses.window = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.mk_pad()

    def mk_pad(self) -> _curses.window:
        pad = curses.newpad(self.nlines, self.ncols)
        pad.box()
        self.pad = pad
        self.addstr(0, 5, self.name)
        return pad

    def addstr(self, *args) -> None:
        self.pad.addstr(*args)
        return

    def noutrefresh(self) -> None:
        self.pad.noutrefresh(
            0, 0, self.y, self.x,
            self.y + self.nlines, self.x+self.ncols)
        return


words = list('升级到专业版来无限制访问所有模型和并解锁高级功能。专业版无限制访问所有模型更快响应速度实时网络访问阅读任何网页和')
words1 = '升级到专业版来无限制访问所有模型和并解锁高级功能。专业版无限制访问所有模型更快响应速度实时网络访问阅读任何网页和'


def main(screen: _curses.window):
    # Clear screen
    screen.clear()
    screen.box()
    screen.noutrefresh()

    kwargs = dict(
        nlines=4,
        ncols=80,
        y=0,
        x=0,
        name='Prompt pad'
    )
    pad0 = CursesPad(**kwargs)
    pad0.addstr(1, 1, f'Prompt | {pref_encoding} >>')
    pad0.noutrefresh()

    kwargs = dict(
        nlines=10,
        ncols=80,
        y=5,
        x=0,
        name='Time pad'
    )
    pad1 = CursesPad(**kwargs)
    pad1.addstr(1, 5, f'{tc.s}: {tc.t}')
    pad1.noutrefresh()

    def loop():
        while True:
            tc.tick()
            pad1.addstr(1, 5, f'{tc.s}: {tc.t}')
            pad1.noutrefresh()
            curses.setsyx(0, 0)
            curses.doupdate()
            time.sleep(0.01)
    Thread(target=loop, daemon=True).start()

    curses.doupdate()

    prompts = []
    idx = 0
    while True:
        idx += 1
        num = pad0.pad.getch()
        key_name = curses.keyname(num)
        name = keyboard.get_hotkey_name(chr(num))

        if name == 'esc':
            break

        if name == 'backspace':
            if prompts:
                prompts.pop()

        np.random.shuffle(words)
        if len(name) == 1:
            prompts.append(name)

        # It disappears Chinese chars sometimes
        s = 'Prompt | {} >> {} |'.format(idx, ''.join(prompts))
        print(s)

        tic = time.time()
        pad0.addstr(1, 1, s)
        pad0.addstr(2, 1, 'Prompt >> ')
        # Type the Chinese chars one-by-one
        for i, e in enumerate(prompts):
            pad0.pad.addch(e)
            print(i, e, wcswidth(e))
            if wcswidth(e) == 2:
                pad0.pad.addch(f'{wcswidth(e)}')
                # pad0.pad.addch(' ')
                continue
        toc = time.time()
        pad0.pad.addstr(f' | {toc-tic:0.8f}', 10)
        pad0.noutrefresh()
        curses.setsyx(0, 0)
        curses.doupdate()
        curses.napms(1)
        print(prompts)

    return 0


# %% ---- 2024-11-18 ------------------------
# Play ground

if __name__ == "__main__":
    sys.exit(wrapper(main))

# %% ---- 2024-11-18 ------------------------
# Pending


# %% ---- 2024-11-18 ------------------------
# Pending
