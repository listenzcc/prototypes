from threading import Thread
from nicegui import ui


if __name__ == "__main__":
    ui.label('Hello NiceGUI!')
    # Thread(target=ui.run, daemon=True).start()
    ui.run()
    input('>>')
