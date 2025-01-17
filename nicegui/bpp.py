from nicegui import ui, events
import json
import requests
import pandas as pd


def my_table():
    # Define columns
    columns = [
        {'name': 'action', 'label': 'Action', 'field': 'action',
            'required': True, 'align': 'left'},
        {'name': 'Group', 'label': 'Group', 'field': 'Group',
            'required': True, 'align': 'left'},
    ]

    rows = [
        {'id': None, 'action': False, 'Group': 'A'},
        {'id': None, 'action': True, 'Group': 'B'},
        {'id': None, 'action': True, 'Group': 'C'},
        {'id': None, 'action': True, 'Group': 'D'},
    ]
    # Create the table with defined columns, add df data to table
    table = ui.table(columns=columns, rows=rows,
                     selection=None, pagination=5).classes('w-full')
    Columns_Name = table.columns
    print("Columns Name:", Columns_Name)
    if any(column['label'] == 'Action' for column in table.columns):
        print(f"The table contains the 'Action' column.")
        table.add_slot('body-cell-action', '''
            <q-td key="action" :props="props">
                <q-toggle 
                    :color="props.value ? 'red' : 'green'" 
                    keep-color
                    :label="props.value ? 'Get' : 'Leave'" 
                    checked-icon="clear" 
                    v-model="props.row.action" 
                    v-model="check_value" 
                    @update:model-value="() => $parent.$emit(
                        <!-- callback function -->
                        'action_event', <!-- should match string passed to `table.on` below -->
                        
                        <!-- arguments, can be whatever you want really -->
                        props.row,   <!-- this would pass the whole row of data -->
                        props.row.Group,   <!-- this would pass data of the Group column for this row -->
                        props.value ? 'Get' : 'Leave'  <!-- this will pass a string indicating the action based on the toggle switch state -->
                    )"
                />           
            </q-td>
        ''')
    else:
        print(f"The table does not contain the 'Action' column.")
    with table.add_slot('top-right'):
        with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
            ui.icon('search')
    ui.timer(5.0, lambda: table, active=True)


def handle_action_event(e: events.GenericEventArguments) -> None:
    print(f"{e.sender}")  # this will be the table object
    print(f"{e.args}")  # this will be the args defined in the emit call
    ui.notify(f'{e.args[1]} wants action {e.args[2]}')
    for row in rows:
        if row['id'] == e.args['id']:
            row['name'] = e.args['name']
    ui.notify(f'Table.rows is now: {table.rows}')


ui.timer(1.0, lambda: my_table(), once=True)
ui.run(port=8080)
