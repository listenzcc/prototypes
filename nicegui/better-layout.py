import time
import random
import asyncio
from queue import Queue
from nicegui import ui


class NiceGuiLayout:
    def __init__(self):
        self._layout()
        ui.timer(0.1, self.update_messages)
        ui.run(title='NiceGUIApplication', frameless=False)

    def _layout(self):
        self.label = ui.label('Title label')
        self.log = ui.log(max_lines=10)
        self.button = ui.button('Click me', on_click=self.on_click)
        self.card = ui.card().style('max-height: 600px;')
        with self.card:
            self.spinner = ui.spinner(size='lg')

    async def on_click(self):
        print('Pressed button.')
        self.spinner.set_visibility(False)
        self.card.clear()
        with self.card:
            spinner = ui.spinner(size='lg')
            await asyncio.sleep(1.3)
            ui.label('Button pressed')
            spinner.set_visibility(False)
            del spinner

    def update_messages(self):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        message = f'{timestamp} - Random Value: {random.randint(1, 100)}'
        self.log.push(message)
        ui.update()


ngl = NiceGuiLayout()
