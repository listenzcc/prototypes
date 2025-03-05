"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-02-05
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    How to use the util.py.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-02-05 ------------------------
# Requirements and constants
import time
import keyboard
import win32process
from pywinauto import Application
from rich import print, inspect
from util import get_all_desktops, get_current_desktop
from util import get_app_and_titles, get_current_app
from ui import create_ui, ui, attach_titlebar


# %% ---- 2025-02-05 ------------------------
# Function and class
def get_pid_from_hwnd(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def switch_to_app(app):
    print(f'Switching to {app}')
    pid = get_pid_from_hwnd(app.hwnd)
    print(f'Got pid {pid}')
    app = Application().connect(process=pid)
    app.top_window().set_focus()
    print(f'Switched to {pid} | {app}')


def rolling_all_desktops(interval: float = 1):
    '''
    Slowly rolling thought all the desktops,
    and return the current desktop finally.

    :param interval: the interval to switch from one desktop to another.
    '''
    desktops = get_all_desktops()
    current = desktops[0].current()
    for desktop in desktops:
        desktop.go()
        print(f'Switched to {desktop}')
        time.sleep(interval)
    current.go()
    print(f'Switched back to {current}')


def rolling_all_apps(interval: float = 1, current_desktop=True):
    apps = get_app_and_titles(current_desktop)
    current_app = get_current_app()

    for app in apps:
        app.desktop.go()
        app.set_focus()
        print(f'Switched to {app}')
        time.sleep(interval)

    current_app.desktop.go()
    current_app.set_focus()
    print(f'Switched back to {app}')


def suppress_event(e):
    return False


# %% ---- 2025-02-05 ------------------------
# Play ground
if __name__ in ['__main__', '1__mp_main__']:
    # Switch through desktops and apps
    # rolling_all_desktops()
    # rolling_all_apps(current_desktop=False)

    print(__name__)

    desktops = get_all_desktops()
    print([e.id for e in desktops])

    current_desktop = get_current_desktop()
    # inspect(current_desktop)

    apps = get_app_and_titles()
    print(apps)
    selected_apps = [e for e in apps if e['title'].endswith(' - Notepad')]
    print(selected_apps)

    current_app = get_current_app()
    # inspect(current_app)

    # Simulation of the keyboard write.
    if True:
        keyboard.hook(suppress_event, suppress=True)
        try:
            app = selected_apps[0]
            switch_to_app(app['app'])
            # app['app'].desktop.go()
            # app['app'].set_focus()
            keyboard.write(f'Start, {time.ctime()}, Stop.\r\n', delay=0.01)
            keyboard.write(f'中文测试\r\n'*10, delay=0.01)
        except IndexError:
            print(f'Nothing for keyboard to write.')
        finally:
            keyboard.unhook_all()
            switch_to_app(current_app)
            # current_app.desktop.go()
            # current_app.set_focus()

    title = 'AppView'
    frameless = True
    if frameless:
        attach_titlebar(title)
    create_ui()
    ui.run(title=title, frameless=frameless, reload=False)


# %% ---- 2025-02-05 ------------------------
# Pending


# %% ---- 2025-02-05 ------------------------
# Pending
