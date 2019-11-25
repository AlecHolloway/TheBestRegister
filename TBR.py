# For PySimpleGUI
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

# For copying lists before clearing them
import copy

# For recording timestamps
import datetime


# User login module
import login

# Admin login module
import admin_login

# Database functionality
from database import database

# Administrator control panel
import admin_panel

# Global variables
historyList = []
historyEntry_default = {
                        'TransactionID' : 'NOT SET',
                        'Location' : '560 Barr Avenue, Mississippi State, MS 39762',
                        'Timestamp' : 'NOT SET',
                        'PaymentTotal' : 'NOT SET',
                        'PaymentInfo' : 'NOT SET',
                        'Items' : 'NOT SET',
                        'this_hash' : 'NOT SET',
                        'next_hash' : 'NOT SET',
                        'previous_hash' : 'NOT SET'
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
    
    # Put each list item on its own line
    separator = '\n'
    stringOutput = separator.join(listInput)
    
    return stringOutput


# Main function
def main():
    # Flags
    access = False
    windowItemActive = False
    windowPayActive = False
    windowReceiptActive = False
    windowHistoryActive = False
    
    # Login event loop
    while True:
        access = login.UserLogin()
        if access == True:
            break
        else:
            return
    
    # Local variables
    priceSum = 0
    payMethod = 'Cash'
    receiptList = []
    receiptEntry = "ITEM\tPRICE"
    itemIDList = []
    historyEntry = copy.deepcopy(historyEntry_default)
    
    # Window setup
    layoutMain = [
                  [sg.Text('Transaction: ', key='_LABEL_', size=(20,1))],
                  [sg.Multiline('', size=(40,20), key='_DISPLAY_')],
                  [sg.Text('Total:', size=(20,1)), sg.Text('0.00', key='_TOTAL_', size=(20,1))],
                  [sg.Button('Scan', bind_return_key=True), sg.Button('Pay'), sg.Button('History')],
                  [sg.Button('Admin Login'), sg.Button('EXIT')]
                 ]

    windowMain = sg.Window('The BEST Register', layoutMain, default_button_element_size=(10,2), auto_size_buttons=False)

    # Register window event Loop
    while True:
        eventMain, valuesMain = windowMain.Read()
        
        # Closing the window
        if eventMain in (None, 'EXIT'):
            windowMain.Close()
            break
        if eventMain in ('Admin Login'):
            if(admin_login.AdminLogin()):
                admin_panel.Panel()
        
        # Scanning items
        if eventMain in ('Scan'):
            if receiptList != []:
                windowMain.Element('_DISPLAY_').Update(listOutput(receiptList))
            else:
                windowMain.Element('_DISPLAY_').Update('')
            
            windowItemActive = True
            
            # Window setup
            layoutItem = [
                          [sg.Text('Exit this window before paying!')],
                          [sg.Button('Sweatshirt'), sg.Button('Hoodie')],
                          [sg.Button('T-shirt'), sg.Button('Cap')],
                          [sg.Button('Jogger'), sg.Button('EXIT')]
                         ]
                  
            windowItem = sg.Window('Select Items', layoutItem, default_button_element_size=(6,2), auto_size_buttons=False)
        
        # Completing a transaction
        if eventMain in ('Pay'):
            if receiptList == []:
                sg.PopupError('There are no scanned items!')
            else:
                windowPayActive = True
                
                # Window setup
                layoutPay = [
                             [sg.Text('Total:\t' + "{0:.2f}".format(priceSum))],
                             [sg.Button('Cash'), sg.Button('Check')],
                             [sg.Button('Credit'), sg.Button('Debit')],
                             [sg.Button('EXIT')]
                            ]
                      
                windowPay = sg.Window('Payment Method', layoutPay, default_button_element_size=(6,2), auto_size_buttons=False)
        
        # Accessing the transaction history
        if eventMain in ('History'):
            windowHistoryActive = True
            
            # Window setup
            layoutHistory = [
                             [sg.Multiline('', size=(100,20), key='_HISTORY_')],
                             [sg.Text('Enter search terms: ', size=(40,1))],
                             [sg.Input(size=(40,1), key='_SEARCH_', do_not_clear=True)],
                             [sg.Radio('Transaction ID', 1, True, key='_TID_'), sg.Radio('Location', 1, key='_L_')],
                             [sg.Radio('Pay Info', 1, key='_PI_'), sg.Radio('Item ID', 1, key='_IID_')],
                             [sg.Button('Search'), sg.Button('EXIT')],
                             [sg.Text('Start Date (Ex: November 18, 2019) *Inclusive*: ', size=(35,1)), sg.Text('End Date(Ex: November 19, 2019) *Non-inclusive*: ', size=(40,1))],
                             [sg.Input(size=(40,1), key='_SDATE_', do_not_clear=True), sg.Input(size=(40,1), key='_EDATE_', do_not_clear=True)]
                            ]
                  
            windowHistory = sg.Window('Transaction History', layoutHistory, default_button_element_size=(6,2), auto_size_buttons=False)
            
        # Buttons for debugging
        if eventMain in ('receiptList'):
            print(f"receiptList: {receiptList}")
        if eventMain in ('historyList'):
            print(f"historyList: {historyList}")
        # Item selection window event loop
        while windowItemActive:
            eventItem, valuesItem = windowItem.Read()
            
            if eventItem in (None, 'EXIT'):
                windowItemActive = False
                windowItem.Close()
                break
            
            if eventItem in ('Hoodie', 'Sweatshirt', 'T-shirt', 'Cap', 'Jogger'):
                priceValue = priceDict[eventItem][1]
                receiptEntry = '(' + priceDict[eventItem][0] + ')  ' + eventItem + '  ' + priceValue
                
                priceSum += float(priceValue)
                windowMain.Element('_TOTAL_').Update("{0:.2f}".format(priceSum))
                
                itemIDList.append(priceDict[eventItem][0])
                receiptList.append(receiptEntry)
                windowMain.Element('_DISPLAY_').Update(listOutput(receiptList))
                
                
        # History window event loop
        while windowHistoryActive:
            eventHistory, valuesHistory = windowHistory.Read()
            
            if eventHistory in (None, 'EXIT'):
                windowHistoryActive = False
                windowHistory.Close()
                break
            
            if eventHistory in ('Search'):
                if valuesHistory['_TID_']:
                    criteria = 'TransactionID'
                elif valuesHistory['_L_']:
                    criteria = 'Location'
                elif valuesHistory['_PI_']:
                    criteria = 'PaymentInfo'
                elif valuesHistory['_IID_']:
                    criteria = 'Items'
                    
                term = valuesHistory['_SEARCH_']
                startDate = valuesHistory['_SDATE_']
                endDate = valuesHistory['_EDATE_']
                
                display = database.search_database(criteria, term, startDate, endDate)
                windowHistory.Element('_HISTORY_').Update(display)
                
        
        # Payment window event loop
        while windowPayActive:
            eventPay, valuesPay = windowPay.Read()
            
            if eventPay in (None, 'EXIT'):
                windowPayActive = False
                windowPay.Close()
                break
            
            if eventPay in ('Cash', 'Check', 'Credit', 'Debit'):
                payMethod = eventPay

                # Change date format to excluse hours/minutes
                dt = datetime.datetime.now()
                timestamp = dt.strftime("%B %d, %Y")
                
                historyEntry['Timestamp'] = timestamp
                historyEntry['PaymentTotal'] = "{0:.2f}".format(priceSum)
                historyEntry['PaymentInfo'] = payMethod
                historyEntry['Items'] = copy.deepcopy(itemIDList)
                
                windowMain.Element('_TOTAL_').Update("0.00")
                
                historyList.append(copy.deepcopy(historyEntry))
                windowMain.Element('_DISPLAY_').Update(['Added to History'])
                
                # Update database
                database.update_database(historyEntry)
                
                # Close window after selection
                windowPayActive = False
                windowPay.Close()
                
                # Print receipt
                layoutReceipt = [
                                 [sg.Text('Transaction ID:\t' + historyEntry['TransactionID'])],
                                 [sg.Text('Date:\t' + historyEntry['Timestamp'])],
                                 [sg.Text('Store:\t' + historyEntry['Location'])],
                                 [sg.Text('Paid with:\t' + historyEntry['PaymentInfo'])],
                                 [sg.Text(listOutput(receiptList))],
                                 [sg.Text('Total Purchase:\t' + historyEntry['PaymentTotal'])],
                                 [sg.Button('EXIT')]
                                ]
                      
                windowReceipt = sg.Window('Receipt', layoutReceipt, default_button_element_size=(6,2), auto_size_buttons=False)
                windowReceiptActive = True
                
                
                # Receipt window event loop
                while windowReceiptActive:
                    eventReceipt, valuesReceipt = windowReceipt.Read()
                    
                    if eventReceipt in (None, 'EXIT'):
                        windowReceiptActive = False
                        windowReceipt.Close()
                        break
                
                # Reset variables
                priceSum = 0
                historyEntry = copy.deepcopy(historyEntry_default)
                itemIDList.clear()
                receiptList.clear()
                
                # Exit event loop
                break
    

if __name__ == '__main__':
	main()
