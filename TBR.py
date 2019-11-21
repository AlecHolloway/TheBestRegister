# For PySimpleGUI
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

# For copying lists before clearing them
import copy

# For recording timestamps
from datetime import datetime as dt

# User login module
import login

# Global variables
historyList = []
historyEntry_default = {
                        'TransactionID' : 'NOT SET',
                        'Location' : '560 Barr Avenue, Mississippi State, MS 39762',
                        'Timestamp' : 'NOT SET',
                        'PaymentTotal' : 'NOT SET',
                        'PaymentInfo' : 'NOT SET',
                        'Items' : 'NOT SET'
                       }

# For each item, there is an item ID and a price
priceDict = {
             'Hoodie' : ('HOOD001','20.99'),
             'Sweatshirt' : ('SWTS001','14.99'),
             'T-shirt' : ('TSHR001','10.99'),
             'Cap' : ('CAP001','12.99'),
             'Jogger' : ('JOGR001','29.99')
            }


# Output a list as a string
def listOutput(listInput):
    
    if isinstance(listInput[len(listInput)-1], list):
        for i in range(len(listInput)):
            # Convert each nested list into a string
            listInput[i] = listOutput(listInput[i])
    
    print(f"listInput: {listInput}")
    
    # Put each list item on its own line
    separator = '\n'
    stringOutput = separator.join(listInput)
    
    # Check output in the console
    print(f"stringOutput: {stringOutput}")
    
    return stringOutput


# Main function
def main():
    # Flags
    access = False
    windowItemActive = False
    windowPayActive = False
    
    # Login event loop
    while True:
        access = login.UserLogin()
        if access == True:
            break
        else:
            return
    
    # Local variables
    transactionCount = 0
    priceSum = 0
    payMethod = 'Cash'
    receiptList = []
    receiptEntry = "ITEM\t\tPRICE"
    historyEntry = historyEntry_default
    
    # Window setup
    layoutMain = [
                  [sg.Text('Receipt: ', key='_LABEL_')],
                  [sg.Multiline('', size=(40,20), key='_ITEM_LIST_')],
                  
                  # Manual item entry
                  # [sg.Text('Item: ', size=(20,1), key='_INPUT_LABEL_1_'), sg.Text('Price: ', size=(20,1), key='_INPUT_LABEL_2_')],
                  # [sg.Input(size=(20,1), key='_ITEM_IN_', do_not_clear=False), sg.Input(size=(20,1), key='_PRICE_IN_', do_not_clear=False)],
                  
                  [sg.Button('Scan', bind_return_key=True), sg.Button('Pay'), sg.Button('History')],
                  [sg.Button('EXIT')],
                  
                  # Buttons for debugging
                  # [sg.Button('receiptList'), sg.Button('historyList')]
                 ]

    windowMain = sg.Window('The BEST Register', layoutMain, default_button_element_size=(10,2), auto_size_buttons=False)

    # Register event Loop
    while True:
        eventMain, valuesMain = windowMain.Read()
        
        # Check values in the console
        print('\n', eventMain, valuesMain)
        
        # Closing the window
        if eventMain in (None, 'EXIT'):
            windowMain.Close()
            break
        
        # Scanning items
        if eventMain in ('Scan'):
            windowItemActive = True
            
            # Window setup
            layoutItem = [
                          [sg.Button('Sweatshirt'), sg.Button('Hoodie')],
                          [sg.Button('T-shirt'), sg.Button('Cap')],
                          [sg.Button('Jogger'), sg.Button('EXIT')]
                         ]
                  
            windowItem = sg.Window('Preset Items', layoutItem, default_button_element_size=(6,2), auto_size_buttons=False)
            
            # if valuesMain['_ITEM_IN_'] == '' or valuesMain['_PRICE_IN_'] == '':
                # sg.PopupError('Need item name and price!')
            # else:
                # priceValue = float(valuesMain['_PRICE_IN_'])
                # receiptEntry = valuesMain['_ITEM_IN_'] + '\t\t' + "{0:.2f}".format(priceValue)
                
                # priceSum += priceValue
                
                # receiptList.append(receiptEntry)
                # windowMain.Element('_LABEL_').Update('Receipt: ')
                # windowMain.Element('_ITEM_LIST_').Update(listOutput(receiptList))
        
        # Completing a transaction
        if eventMain in ('Pay'):
            if receiptList == []:
                sg.PopupError('There are no scanned items!')
            else:
                windowPayActive = True
                
                # Window setup
                layoutPay = [
                              [sg.Text('Total:\t\t' + "{0:.2f}".format(priceSum))],
                              [sg.Button('Cash'), sg.Button('Check')],
                              [sg.Button('Credit'), sg.Button('Debit')],
                              [sg.Button('EXIT')]
                            ]
                      
                windowPay = sg.Window('Preset Items', layoutPay, default_button_element_size=(6,2), auto_size_buttons=False)
        
        # Accessing the transaction history
        if eventMain in ('History'):
            windowMain.Element('_LABEL_').Update('History: ')
            windowMain.Element('_ITEM_LIST_').Update(historyList)
            
        # Buttons for debugging
        if eventMain in ('receiptList'):
            print(f"receiptList: {receiptList}")
        if eventMain in ('historyList'):
            print(f"historyList: {historyList}")
        
        # Item selection window
        while windowItemActive:
            eventItem, valuesItem = windowItem.Read()
            
            if eventItem in (None, 'EXIT'):
                windowItemActive = False
                windowItem.Close()
                break
            
            if eventItem in ('Hoodie', 'Sweatshirt', 'T-shirt', 'Cap', 'Jogger'):
                priceValue = priceDict[eventItem][1]
                receiptEntry = eventItem + '\t\t' + priceValue
                
                priceSum += float(priceValue)
                
                receiptList.append(receiptEntry)
                windowMain.Element('_LABEL_').Update('Receipt: ')
                windowMain.Element('_ITEM_LIST_').Update(listOutput(receiptList))
                
        # Payment type selection window
        while windowPayActive:
            eventPay, valuesPay = windowPay.Read()
            
            if eventPay in (None, 'EXIT'):
                windowPayActive = False
                windowPay.Close()
                break
            
            if eventPay in ('Cash', 'Check', 'Credit', 'Debit'):
                payMethod = eventPay
            
                transactionCount += 1
                
                historyEntry['TransactionID'] = transactionCount
                historyEntry['Timestamp'] = str(dt.now())
                historyEntry['PaymentTotal'] = "{0:.2f}".format(priceSum)
                historyEntry['PaymentInfo'] = payMethod
                historyEntry['Items'] = copy.deepcopy(receiptList)
                
                historyList.append(copy.deepcopy(historyEntry))
                windowMain.Element('_LABEL_').Update('Receipt: ')
                windowMain.Element('_ITEM_LIST_').Update(['Added to History'])
                
                # Reset variables
                priceSum = 0
                historyEntry = historyEntry_default
                receiptList.clear()
                
                # Close window after selection
                windowPayActive = False
                windowPay.Close()
                break
    

if __name__ == '__main__':
	main()