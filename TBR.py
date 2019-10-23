import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
    
receiptList = []
historyList = []


def listOutput(listInput):
    
    if isinstance(listInput[0], list):
        for eachList in listInput:
            # Convert each list into a string
            eachList = listOutput(eachList)
    
    separator = ', '
    stringOutput = separator.join(listInput)
    
    return stringOutput


layout = [[sg.Text('Receipt: ', key='_LABEL_'), sg.Text('(Empty)', key='_OUTPUT_') ],
          [sg.Input(key='_IN_', do_not_clear=False)],
          [sg.Button('Scan'), sg.Button('Receipt'), sg.Button('History'), sg.Button('Exit')]]

window = sg.Window('The BEST Register', layout)

while True:                 # Event Loop
    event, values = window.Read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event in ('Scan'):
        receiptList.append(values['_IN_'])
        window.Element('_LABEL_').Update('Receipt: ')
        window.Element('_OUTPUT_').Update(listOutput(receiptList))
    if event in ('Receipt'):
        historyList.append(receiptList)
        window.Element('_LABEL_').Update('Receipt: ')
        window.Element('_OUTPUT_').Update('Added to History')
        receiptList.clear()
    if event in ('History'):
        window.Element('_LABEL_').Update('History: ')
        window.Element('_OUTPUT_').Update(listOutput(historyList))
window.Close()