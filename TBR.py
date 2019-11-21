import sys
from datetime import datetime as dt
import copy
from decimal import *
getcontext().prec = 2

import login

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

historyList = []
historyEntry_default = {
                        'Location' : 'NOT SET',
                        'Timestamp' : 'NOT SET',
                        'Total' : 'NOT SET',
                        
                       }
priceDict = {
             'Hoodie' : '20.99',
             'Sweatshirt' : '14.99',
             'T-shirt' : '10.99',
             'Cap' : '12.99',
             'Jogger' : '29.99'
            }


def listOutput(listInput):
    
    if isinstance(listInput[len(listInput)-1], list):
        for i in range(len(listInput)):
            # Convert each list into a string
            listInput[i] = listOutput(listInput[i])
    
    print(f"listInput: {listInput}")
    
    separator = '\n'
    stringOutput = separator.join(listInput)
    
    print(f"stringOutput: {stringOutput}")
    
    return stringOutput


def main():
    access = False
    windowItemActive = False
    
    while True:
        access = login.UsernameEnter()
        if access == True:
            break
        else:
            return
    
    receiptList = []
    receiptEntry = "ITEM\t\tPRICE"
    historyEntry = {
                   }
                   
    layoutMain = [[sg.Text('Receipt: ', key='_LABEL_')],
                  [sg.Multiline('', size=(40,20), key='_ITEM_LIST_')],
                  [sg.Text('Item: ', size=(20,1), key='_INPUT_LABEL_1_'), sg.Text('Price: ', size=(20,1), key='_INPUT_LABEL_2_')],
                  [sg.Input(size=(20,1), key='_ITEM_IN_', do_not_clear=False), sg.Input(size=(20,1), key='_PRICE_IN_', do_not_clear=False)],
                  [sg.Button('Scan', bind_return_key=True), sg.Button('Receipt'), sg.Button('History'), sg.Button('EXIT')],
                  [sg.Button('Choose Items'), sg.Button('receiptList'), sg.Button('historyList')]]

    windowMain = sg.Window('The BEST Register', layoutMain, default_button_element_size=(6,2), auto_size_buttons=False)

    while True:                 # Event Loop
        eventMain, valuesMain = windowMain.Read()
        
        # Check values in the console
        print('\n', eventMain, valuesMain)
        
        if eventMain in (None, 'EXIT'):
            windowMain.Close()
        if eventMain in ('Scan'):
            if valuesMain['_ITEM_IN_'] == '' or valuesMain['_PRICE_IN_'] == '':
                sg.PopupError('Need item name and price!')
            else:
                priceValue = valuesMain['_PRICE_IN_']
                receiptEntry = valuesMain['_ITEM_IN_'] + '\t\t' + "{0:.2f}".format(float(priceValue))
                receiptList.append(receiptEntry)
                windowMain.Element('_LABEL_').Update('Receipt: ')
                windowMain.Element('_ITEM_LIST_').Update(listOutput(receiptList))
        if eventMain in ('Receipt'):
            if receiptList == []:
                sg.PopupError('There are no scanned items!')
            else:
                historyEntry['Location'] = 'NOT SET'
                historyList.append(copy.deepcopy(receiptList))
                windowMain.Element('_LABEL_').Update('Receipt: ')
                windowMain.Element('_ITEM_LIST_').Update(['Added to History'])
                receiptList.clear()
        if eventMain in ('History'):
            windowMain.Element('_LABEL_').Update('History: ')
            windowMain.Element('_ITEM_LIST_').Update(historyList)
        if eventMain in ('Choose Items'):
            windowItemActive = True
            
            layoutItem = [[sg.Button('Sweatshirt'), sg.Button('Hoodie')],
                          [sg.Button('T-shirt'), sg.Button('Cap')],
                          [sg.Button('Jogger'), sg.Button('EXIT')]]
                  
            windowItem = sg.Window('Preset Items', layoutItem, default_button_element_size=(6,2), auto_size_buttons=False)
        if eventMain in ('receiptList'):
            print(f"receiptList: {receiptList}")
        if eventMain in ('historyList'):
            print(f"historyList: {historyList}")
            
        while windowItemActive:
            eventItem, valuesItem = windowItem.Read()
            if eventItem in (None, 'EXIT'):
                windowItemActive = False
                windowItem.Close()
            if eventItem in ('Hoodie', 'Sweatshirt', 'T-shirt', 'Cap', 'Jogger'):
                receiptEntry = eventItem + '\t\t' + priceDict[eventItem]
                receiptList.append(receiptEntry)
                windowMain.Element('_LABEL_').Update('Receipt: ')
                windowMain.Element('_ITEM_LIST_').Update(listOutput(receiptList))
    

if __name__ == '__main__':
	main()