import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
    
import copy
    
receiptList = []
historyList = []


def listOutput(listInput):
    
    if isinstance(listInput[len(listInput)-1], list):
        for i in range(len(listInput)):
            # Convert each list into a string
            
            # print(f"listInput[{i}] PRE-RECURSION: {listInput[i]}")
            # print(f"listInput PRE-RECURSION: {listInput}")
            # print("RECURSING")
            
            listInput[i] = listOutput(listInput[i])
            
            # print(f"listInput[{i}] POST-RECURSION: {listInput[i]}")
            # print(f"listInput POST-RECURSION: {listInput}")
    
    print(f"listInput: {listInput}")
    
    separator = ', '
    stringOutput = separator.join(listInput)
    
    print(f"stringOutput: {stringOutput}")
    
    return stringOutput


layout = [[sg.Text('Receipt: ', key='_LABEL_'), sg.Text('(Empty)', key='_OUTPUT_') ],
          [sg.Input(key='_IN_', do_not_clear=False)],
          [sg.Button('Scan'), sg.Button('Receipt'), sg.Button('History'), sg.Button('Exit')],
          [sg.Button('receiptList'), sg.Button('historyList')]]

window = sg.Window('The BEST Register', layout)

while True:                 # Event Loop
    event, values = window.Read()
    print('\n', event, values)
    if event in (None, 'Exit'):
        break
    if event in ('Scan'):
        receiptList.append(values['_IN_'])
        window.Element('_LABEL_').Update('Receipt: ')
        window.Element('_OUTPUT_').Update(listOutput(copy.copy(receiptList)))
    if event in ('Receipt'):
        historyList.append(copy.deepcopy(receiptList))
        window.Element('_LABEL_').Update('Receipt: ')
        window.Element('_OUTPUT_').Update('Added to History')
        receiptList.clear()
    if event in ('History'):
        window.Element('_LABEL_').Update('History: ')
        window.Element('_OUTPUT_').Update(listOutput(copy.copy(historyList)))
    if event in ('receiptList'):
        print(f"receiptList: {receiptList}")
    if event in ('historyList'):
        print(f"historyList: {historyList}")
window.Close()