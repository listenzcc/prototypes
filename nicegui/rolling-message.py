from nicegui import ui
import random
import time
from frameless_util import attach_titlebar


messages = []


def update_messages():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    message = f'{timestamp} - Random Value: {random.randint(1, 100)}'
    messages.insert(0, message)  # Insert the new message at the beginning
    if len(messages) > 10:  # Keep only the last 10 messages
        messages.pop()
    log.clear()  # Clear the log content
    for msg in messages:
        log.push(msg)
    ui.update()


log = ui.log(max_lines=10)
with ui.card() as card:
    spinner = ui.spinner(size='lg')
    ui.label('Card 1')

ui.timer(1.0, update_messages)

window_title = 'NiceGUIApplication'

frameless = False
if frameless:
    attach_titlebar(window_title)

ui.run(title=window_title, frameless=frameless)
