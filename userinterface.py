
import PySimpleGUI as sg      

sg.theme('DarkAmber')    # Keep things interesting for your users
cells =  [[sg.Input(str(i), justification="center", enable_events=True, size=(4,2), key=(i,j)) for i in range(8)
] for j in range(8)]
cellKeys = [(i,j) for i in range(8) for j in range(8)]
print(cellKeys)

layout = [[sg.Text('Persistent window')], [sg.Button('Read'), sg.Exit()]]+cells      

window = sg.Window('Window that stays open', layout)      

while True:                             # The Event Loop
    event, values = window.read() 
    if event in cellKeys:
        print(event, values[event])
        if values[event]:
            window[event].update(value=values[event][-1],move_cursor_to=1)
            window.refresh()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      

window.close()
