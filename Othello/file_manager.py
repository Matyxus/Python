import PySimpleGUI as sg
sg.theme('Dark Brown')
event, values = sg.Window('Game settings', [[sg.Text('Select ->'), sg.Listbox(['Vs AI', 'Start as White', 'Start as Black'], 
	select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, 3), key='LB')],
    [sg.Button('Ok'), sg.Button('Cancel')]]).read(close=True)

if event == 'Ok':
    sg.popup(f'You chose {values["LB"]}')
else:
    sg.popup_cancel('User aborted')

#sg.theme_previewer()