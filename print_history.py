import sys

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import hashlib
import datetime
import hashlib
import string
from pygrok import Grok
import time
from datetime import datetime as dt

#imports for database
import pymongo
import motor
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://chapiiin:password20@cluster0-6dsmr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.TBR
transactions = db.transactions


def RetAll():
    
    #Find the last transaction
    last_doc = transactions.find().sort('_id', pymongo.DESCENDING).limit(1)

    #Find the last transaction ID
    for x in last_doc:
        print("Last transaction: ", x)
    lastTransactionID = x['_id']
    print("Last transaction ID: ", lastTransactionID)
    print()
    print()
    
    history_array = []
    item_num = 1
    for x in range(lastTransactionID):
    #result = transactions.find()
    
        start = transactions.find({"_id":item_num})
    
        for i in start:
            
            a = ('ID:', i['_id'])
            b = ('Items Purchased:', i['Items purchased'])        
            c = ('Timestamp:', i['Timestamp'])
            d = ('Transaction hash:', i['Transaction hash'])
            e = ('Store Location:', i['Store Location'])        
            f = ('Cost:', i['Cost'])
            g = ('Payment Method:', i['Payment Method'])  
            h = ('')

            history_array.extend([a,'\n',b,'\n',c,'\n',d,'\n',e,'\n',f,'\n',g,'\n',h,'\n'])
        item_num += 1
    return history_array

        
            
def main():
    
    column = [[sg.Text('stupid2', justification='center', size=(50,1))]]

    layout5 = [[sg.Text('Below is the printed history', size=(20,1), font='Helvetica, 18')],
    [sg.Listbox(values=(RetAll()), size=(120,120))],
    ] 

    window = sg.Window('stupid1', layout5, default_element_size=(20, 1), grab_anywhere=False, size=(700,700))
    while True:
        ev, va = window.Read()


main()
