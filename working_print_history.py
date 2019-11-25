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
db = client.TestTBR
transactions = db.transactions


def RetAll():
    
    #Find the last transaction
    last_doc = transactions.find().sort('TransactionID', pymongo.DESCENDING).limit(1)

    #Find the last transaction ID
    for x in last_doc:
        print("Last transaction: ", x)
    lastTransactionID = x['TransactionID']
    print()
    print()
    
    history_array = []
    item_num = "1"

    lastTransactionID = int(lastTransactionID)
    print("Last transaction ID: ", lastTransactionID)
    for x in range(lastTransactionID):
    #result = transactions.find()
        item_num = str(item_num)
    
        start = transactions.find({"TransactionID":item_num})
    
        for i in start:
            
            a = ('ID:', i['TransactionID'])
            b = ('Items:', i['Items'])        
            c = ('Timestamp:', i['Timestamp'])
            #d = ('Transaction hash:', i['this_hash'])
            e = ('Store Location:', i['Location'])        
            f = ('Transaction Cost:', i['PaymentTotal'])
            g = ('Payment Method:', i['PaymentInfo'])  
            h = ('')

            history_array.extend([a,'\n',b,'\n',c,'\n',e,'\n',f,'\n',g,'\n',h,'\n'])
        item_num = int(item_num) + 1
    return history_array

        
            
def main():
    
    column = [[sg.Text('stupid2', justification='center', size=(50,1))]]

    layout5 = [[sg.Text('Below is the printed history', size=(24,1), font='Helvetica, 18')],
    [sg.Listbox(values=(RetAll()), size=(120,120))],
    ] 

    window = sg.Window('TBR', layout5, default_element_size=(20, 1), grab_anywhere=False, size=(800,700))
    while True:
        ev, va = window.Read()


main()
