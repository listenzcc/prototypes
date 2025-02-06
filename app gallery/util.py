"""
File: util.py
Author: Chuncheng Zhang
Date: 2025-02-05
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Application utilities in Windows OS.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-02-05 ------------------------
# Requirements and constants
import pyvda
import win32gui


# %% ---- 2025-02-05 ------------------------
# Function and class
def get_all_desktops():
    '''
    Get all virtual desktops.
    https://github.com/Ciantic/VirtualDesktopAccessor

    :returns: list of virtual desktops.
    '''
    desktops: list = pyvda.get_virtual_desktops()
    return desktops


def get_current_desktop():
    '''
    Get the current virtual desktop.

    :returns: virtual desktop.
    '''
    return get_all_desktops()[0].current()


def switch_to_desktop(desktop):
    '''
    Switch to desktop.

    :param desktop: desktop to switch to.
    '''
    desktop.go()


def get_current_app():
    '''
    Get the current app.

    :return: current app.
    '''
    return pyvda.AppView.current()


def get_app_and_titles(current_desktop=True):
    """
    Retrieves a list of applications and their corresponding titles along with a flag indicating the current application.

    :params current_desktop (bool): If True, only applications on the current desktop are considered. If False, all applications are considered.

    :returns list: A list of dictionaries, where each dictionary contains the following keys:
        - app: The AppView object representing the application.
        - title: The title of the application window.
        - currentFlag: A boolean indicating whether the application is the current application.
    """
    # Get all the applications
    applications = pyvda.get_apps_by_z_order(current_desktop=current_desktop)

    # Remember the current application
    current_application = pyvda.AppView.current()

    # Get the titles
    res = [dict(
        app=e,
        title=get_title(e),
        currentFlag=e == current_application)
        for e in applications]

    return res


def get_title(app: pyvda.AppView) -> str:
    """
    Returns the title of the given application window.

    :param app: The AppView object representing the application window.

    :returns: The title of the application window.
    """

    title: str = win32gui.GetWindowText(app.hwnd)
    return title
# %% ---- 2025-02-05 ------------------------
# Play ground


# %% ---- 2025-02-05 ------------------------
# Pending


# %% ---- 2025-02-05 ------------------------
# Pending
