import login
import sys
from TBRproject import Block,Blockchain, database, search
from datetime import datetime as dt

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

##instance of block and blockchain
block = Block(0,0,0)
blockchain = Blockchain()
search_database = search()
 
 
layout = [[sg.Text('', size=(20,1),font='Helvetica, 18', text_color='red',key='out')],
          [sg.Listbox('', size=(10,5), font='Helvetiva, 18', text_color='black',key='Qty'), sg.Listbox('', size=(10,5), font='Helvetiva, 18', text_color='black',key='name')],  
          [sg.InputText('Enter your price here.', size=(40, 5), justification='right', key='input')],
          [sg.Button('SweatShirt', size=(10,1)), sg.Button('Hoodie', size=(10,1))],
          [sg.Button('T-Shirt', size=(10,1)), sg.Button('Cap', size=(10,1))],
          [sg.Button('Jogger', size=(10,1)), sg.Button('Total', size=(10,1))],
          [sg.Button('Submit',size=(10,1)), sg.Button('Add Item', size=(10,1)), sg.Button('Remove Item', size=(10,1)), sg.Button('Clear')],

          [sg.Button('BlockChain',size=(10,1))]]
          

window = sg.Window('THE BEST REGISTER', layout, default_button_element_size=(5,2), auto_size_buttons=False)

listObject = []
sum = 0
counter = 0
x = 0
total_cost = 0
#QuantityObject = []
# Loop forever reading the window's values, updating the Input field
keys_entered = ''
while True:
    event, values = window.read()  # read the window
    if event is None:  # if the X button clicked, just exit
        break
    if event == 'Clear':  # clear keys if clear button
        keys_entered = ''
        sum = 0
        listObject = []
        window['out'].update(sum)
        
    if event == 'Hoodie':
      keys_entered = '20.99'
      listObject.append('Hoodie')
      window['name'].update(listObject)
      total_cost += 20.99
      
    if event == 'SweatShirt':
      keys_entered = '14.99'
      listObject.append('SweatShirt')
      window['name'].update(listObject)
      total_cost += 14.99

    if event == 'T-Shirt':
      keys_entered = '10.99'
      listObject.append('T-Shirt')
      window['name'].update(listObject)
      total_cost += 10.99
    
    if event == 'Cap':
      keys_entered = '12.99'
      listObject.append('Cap')
      window['name'].update(listObject)
      total_cost += 12.99
      

    if event == 'Jogger':
      keys_entered = '29.99'
      listObject.append('Jogger')
      window['name'].update(listObject)
      total_cost += 29.99
      
    elif event in '1234567890':
        keys_entered = values['input']  # get what's been entered so far
        keys_entered += event  # add the new digit
        
    elif event == 'Submit':
        keys_entered = values['input']
        window['out'].update(keys_entered) 
        # output the final string
        ##adds listobject to a block in the blockchain
        method = str(input("How to pay? credit/cash"))
        if method == 'cash':
            payment = 'cash'
        elif method == 'credit':
            payment = str(input("enter card number: "))

        counter = counter + 1
        string_list = ','

        s = string_list.join(listObject)
        str(total_cost)
        database.update_database(counter ,s, total_cost, payment)
        x = x + 1

        listObject = []
    elif event == 'Add Item':
        keys_entered = values['input']
        sum += float(keys_entered)
        window['out'].update(sum)
        
    elif event == 'Remove Item':
        keys_entered = values['input']
        sum -= float(keys_entered)
        window['out'].update(sum)  
        
    elif event == 'BlockChain':
        answer = str(input("Would you like to search by date or by transaction ID (enter 'date' or 'id'): "))
        if (answer == "id"):
            search.search_id()
        elif (answer == "date"):
            search.search_date
            

    
    #elif event == 'Hoodie', 'SweatShirt', 'Cap', 'T-Shirt', 'Jogger':
       # keys_entered = values['input']
       # Quantity +=  event     
       # window['Qty'].update(Quantity)
        

       ##add item to blockchain
    

    window['input'].update(keys_entered)  # change the window to reflect current key string 
