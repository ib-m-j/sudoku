
import PySimpleGUI as sg      
import numpy
import matplotlib as plt


def getBoard(cellKeys):

    sg.theme('DarkAmber')    # Keep things interesting for your users
    cells =  [[sg.Input( justification="center", enable_events=True, size=(4,2), key=(i,j)) for i in range(8)
    ] for j in range(8)]

    layout = [[sg.Text('Persistent window')], [sg.Button('Read'), sg.Exit()]] +\
             cells +\
             [[sg.Canvas(key='mycanvas',size=(800,100),background_color="white")]]     

    window = sg.Window('Window that stays open', layout, finalize=True)
    window[0,0].set_focus(force=True)
    canvas = window['mycanvas'].TKCanvas
    for i in range(20):
        canvas.create_line(20*i,0,20*i,5*i, width=15)

    print("window created")
    
    returnValue = 'break'
    while True:                             # The Event Loop
        event, values = window.read()
        if event in cellKeys:
            if values[event]:
                window[event].update(value=values[event][-1],move_cursor_to=1)
                window.refresh()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Read':
            returnValue = 'inputOk'
            break

    if returnValue == 'inputOk':
        return [(key, values[key]) for key in cellKeys]
    else:
        window.close()


if __name__ == '__main__':
    print(getBoard())
