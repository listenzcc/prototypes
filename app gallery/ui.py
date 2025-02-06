"""
File: ui.py
Author: Chuncheng Zhang
Date: 2025-02-05
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


# %% ---- 2025-02-05 ------------------------
# Requirements and constants
import win32process
import pygetwindow as gw

from rich import print, inspect
from nicegui import ui, app
from pywinauto import Application

from util import get_all_desktops, get_app_and_titles


# %% ---- 2025-02-05 ------------------------
# Function and class
def get_pid_from_hwnd(hwnd):
    '''
    Get pid of the hwnd.

    :param hwnd (int): the hwnd to get pid from.

    :return (int): the pid of the app.
    '''
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def switch_to_app(app):
    '''
    Switch to the given app.

    app is the dictionary with keys
        - app: the pyvda AppView.
        - title: the title of the app.
        - currentFlag: the boolean flag indicating whether the app is active.

    :param app (dict): the app to switch to.
    '''
    print(f'Switching to {app}')
    inspect(app['app'])
    try:
        # Try to switch to the app.
        app['app'].desktop.go()
        app['app'].set_focus()
    except Exception as e:
        # If failed, try another switching method.
        pid = get_pid_from_hwnd(app['app'].hwnd)
        print(f'Got pid {pid}')
        app = Application().connect(process=pid)
        app.top_window().set_focus()
    print(f'Switched to {app}')


def create_ui():
    row = ui.row()

    @ui.refreshable
    def refresh_ui():
        row.clear()
        with row:  # Use a row to contain all cards
            desktops = get_all_desktops()
            apps = get_app_and_titles(current_desktop=False)
            for desktop in desktops:
                with ui.card().style('max-width: 300px'):
                    # Use CSS for bold text
                    ui.label(f'Desktop {desktop.id}').style(
                        'font-weight: bold;')
                    app_counter = 1  # Initialize app counter
                    for app in apps:
                        if app['app'].desktop.id == desktop.id:
                            title = app['title']
                            if not title:
                                title = '{}'.format(app['app'])

                            def create_label(app_counter, title, app):
                                # The enclosure ensures the label is unique.
                                # Number the apps and add hover animation.
                                label = ui.label(f'{app_counter}. {title}')
                                # Set hover animation.
                                label.style('transition: color 0.3s;').on(
                                    'mouseover', lambda e: label.style('color: blue;')).on(
                                    'mouseout', lambda e: label.style('color: black;')).on(
                                    'click', lambda e, app=app: switch_to_app(app))

                            create_label(app_counter, title, app)
                            app_counter += 1  # Increment app counter
        return

    refresh_ui()
    ui.timer(5, refresh_ui)  # Refresh every 5 seconds


def attach_titlebar(window_title: str = 'NiceGUI', use_mac_style: bool = True) -> None:
    """Title bar

    :param window_title (str): Title of the window.
    :param use_mac_style (bool): True for MacOS style, False for WindowsOS style.
    """
    bgcolor = '#eef5fb'

    def w_close():
        windo = gw.getWindowsWithTitle(window_title)[0]
        windo.close()
        # Shutdown the application nicely.
        app.shutdown()

    def w_min():
        windo = gw.getWindowsWithTitle(window_title)[0]
        windo.minimize()

    def w_max():
        windo = gw.getWindowsWithTitle(window_title)[0]
        windo.maximize()

    def WindowsOS():
        with ui.header().classes(f'w-full h-8 p-2 bg-[{bgcolor}] pywebview-drag-region'):
            with ui.row().classes('gap-1 relative left-[1px] top-[1px] ml-auto mr-0'):
                ui.icon('minimize').classes(
                    'text-[13px] text-black').on('click', w_min)
                ui.icon('crop_square').classes(
                    'text-[13px] text-black').on('click', w_max)
                ui.icon('close').classes(
                    'text-[13px] text-black').on('click', w_close)
            ui.label(window_title).classes(
                'text-sm text-gray-600 absolute left-1/2 top-[6px]').style('transform: translateX(-50%)')

    def MacOS():
        with ui.header().classes(f'w-full h-8 p-2 bg-[{bgcolor}] pywebview-drag-region'):
            with ui.row().classes('gap-1 relative left-[1px] top-[1px]'):
                ui.icon('circle').classes(
                    'text-[13px] text-red-400').on('click', w_close)
                ui.icon('circle').classes(
                    'text-[13px] text-yellow-400').on('click', w_min)
                ui.icon('circle').classes(
                    'text-[13px] text-green-400').on('click', w_max)
            ui.label(window_title).classes(
                'text-sm text-gray-600 absolute left-1/2 top-[6px]').style('transform: translateX(-50%)')

    if use_mac_style == True:
        return MacOS()
    else:
        return WindowsOS()


# %% ---- 2025-02-05 ------------------------
# Play ground


# %% ---- 2025-02-05 ------------------------
# Pending


# %% ---- 2025-02-05 ------------------------
# Pending
