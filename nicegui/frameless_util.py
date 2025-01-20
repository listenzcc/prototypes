from nicegui import ui, app
import pygetwindow as gw

bgcolor = '#eef5fb'


def attach_titlebar(window_title: str = 'NiceGUI', use_mac_style: bool = True) -> None:
    """Title bar

    :param window_title (str): Title of the window.
    :param use_mac_style (bool): True for MacOS style, False for WindowsOS style.
    """

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
