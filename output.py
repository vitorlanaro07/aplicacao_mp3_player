import PySimpleGUI as sg

layout =  [
            [sg.Text('My layout') ],
            [sg.Slider((0,100), tick_interval=10, key='-SLIDER-'),
             sg.Slider((0,100), tick_interval=1000, key='-SLIDER2-')],
            [sg.Button('OK')]
          ]

window = sg.Window('My window', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event is None:
        break