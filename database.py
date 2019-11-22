# Reference used: https://github.com/howCodeORG/Simple-Python-Blockchain/blob/master/blockchain.py
# Reference used: https://stackoverflow.com/questions/20365854/comparing-two-date-strings-in-python
# Reference used: https://thispointer.com/python-how-to-convert-datetime-object-to-string-using-datetime-strftime/
# Instructions to access database: https://realpython.com/introduction-to-mongodb-and-python/

# For PySimpleGUI
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

import datetime
import hashlib
from pygrok import Grok
import time
from datetime import datetime as dt

#imports for database
import pymongo
import motor

client = pymongo.MongoClient("mongodb+srv://chapiiin:password20@cluster0-6dsmr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.TBR

class Block:
    blockNo = 0
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    
    dt = datetime.datetime.now()
    timestampOld = dt.strftime("%B %d, %Y")
    
    TransactionID = 'NOT SET'
    Location = '560 Barr Avenue, Mississippi State, MS 39762'
    Timestamp = 'NOT SET'
    PaymentTotal = 'NOT SET'
    PaymentInfo = 'NOT SET'
    Items = 'NOT SET'

    tbr_dict = {}
    
    def __init__(self, TransactionID, Location, Timestamp, PaymentTotal, PaymentInfo, Items):
        self.TransactionID = TransactionID
        self.Location = Location
        self.Timestamp = Timestamp
        self.PaymentTotal = PaymentTotal
        self.PaymentInfo = PaymentInfo
        self.Items = Items

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.blockNo).encode('utf-8') +
            str(self.TransactionID).encode('utf-8') +
            str(self.Location).encode('utf-8') +
            str(self.Timestamp).encode('utf-8') +
            str(self.PaymentTotal).encode('utf-8') +
            str(self.PaymentInfo).encode('utf-8') +
            str(self.Items).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return (
                "Block Hash: " + str(self.hash()) +
                "\nBlock Number: " + str(self.blockNo) +
                "\nItems: " + str(self.Items) +
                "\nTimestamp: " + str(self.Timestamp) +
                "\nTransaction ID: " + str(self.TransactionID) +
                "\nStore Location: " + str(self.Location) +
                "\nCost: " + int(self.PaymentTotal) +
                "\nPayment: " + str(self.PaymentInfo) +
                "\n--------------"
               )

class Blockchain:
    diff = 20
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)

    block = Block(0,0,0,0,0,["Genesis"])
    dummy = head = block
    head_start = head
    head_start2 = head
    head_start3 = head

    def add(self, block):        
        block.TransactionID = self.block.TransactionID + 1

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1
        
        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1

class database: 
    block = Block(0,0,0,0,0,0)
    blockchain = Blockchain()
    
    #make dictionary callable
    tbr_dict = block.tbr_dict
    transactions = db.transactions
    
    #Function to delete all data from the database
    def empty_database():
        transactions = db.transactions
        print("Emptying database")
        result = transactions.delete_many({})
        print()
        print("Sleeping")
        print()
        time.sleep(1000)

    #function to add entire blockchain to database
    def update_database(counter, entry):
            TransactionID = entry['TransactionID']
            Items = entry['Items']
            Timestamp = entry['Timestamp']
            Location = entry['Location']
            PaymentTotal = entry['PaymentTotal']
            PaymentInfo = entry['PaymentInfo']
    
            blockchain = Blockchain()
            block = Block(0,0,0,0,0,0)
            tbr_dict = block.tbr_dict
            transactions = db.transactions

            #Find the last transaction
            last_doc = transactions.find().sort('TransactionID', pymongo.DESCENDING).limit(1)

            #Find the last transaction ID
            for x in last_doc:
                print("Last transaction: ", x)
            lastTransactionID = x['TransactionID']

            for i in range(lastTransactionID):
                blockchain.add(Block("Null data", 0,0))
                
            #updating dictionary and pushing transactions to database
            while blockchain.head_start2.TransactionID != lastTransactionID:
                blockchain.head_start2 = blockchain.head_start2.next
        
            #add new transaction to blockchain
            blockchain.add(Block(items,cost,payment))

            #move to new transaction
            while blockchain.head_start3.TransactionID != lastTransactionID + 1:
                blockchain.head_start3 = blockchain.head_start3.next

            #update dictionary with new transaction
            print("-ADDING TO DATABASE-")
            block.tbr_dict.update({"TransactionID":blockchain.head_start3.TransactionID})
            block.tbr_dict.update({"Items":blockchain.head_start3.Items})
            block.tbr_dict.update({"Timestamp":blockchain.head_start3.Timestamp})
            block.tbr_dict.update({"Transaction hash":blockchain.head_start3.hash()})
            block.tbr_dict.update({"Location":blockchain.head_start3.Location})
            block.tbr_dict.update({"PaymentTotal":blockchain.head_start3.PaymentTotal})
            block.tbr_dict.update({"PaymentInfo":blockchain.head_start3.PaymentInfo})
            counter += 1
            #push transaction to database
            result2 = transactions.insert_one(block.tbr_dict)

        #temporary counter
           ##counter = 4
           

def search(criteria, term):
    #BE CAREFUL UNCOMMENTING NEXT LINE
#####empty_database()

    transactions = db.transactions
    date_range_array = []

    #make classes callable
    block = Block(0,0,0,0,0,0)
    blockchain = Blockchain()
    
    if criteria in ('TransactionID', 'Location', 'PaymentInfo', 'Items'):
        results = transactions.find({"criteria":term})
        return results

    elif criteria in ('Timestamp'):
        windowDateActive = True
        
        # Window setup
        layoutDate = [
                      [sg.Text('Enter dates as month, day, year \n (Ex: November 18, 2019)', size=(40,2))],
                      [sg.Text('Start date: ', size=(20,1)), sg.Text('End date: ', size=(20,1))],
                      [sg.Input(size=(20,1), key='_START_', do_not_clear=True), sg.Input(size=(20,1), key='_END_', do_not_clear=True)],
                      [sg.Button('Search'), sg.Button('EXIT')]
                     ]
              
        windowDate = sg.Window('Search by Date', layoutDate, default_button_element_size=(6,2), auto_size_buttons=False)
    
    else:
        return "ERROR: INVALID INPUT"
    
    while windowDateActive:
        eventDate, valuesDate = windowDate.Read()
        
        if eventDate in (None, 'EXIT'):
            windowDateActive = False
            windowDate.Close()
            break
        
        if eventDate in ('Search'):
            results = []

            # searching by date
            # declare variables for start and end date
            i = 0.0
            x = valuesDate['_START_']
            y = valuesDate['_END_']

            # print list of dates within range
            start = datetime.datetime.strptime(x, "%B %d, %Y")
            end = datetime.datetime.strptime(y, "%B %d, %Y")
            date_array = \
                (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))

            # Date of transactions within range entered
            for date_object in date_array:
                #print(date_object.strftime("%B %d, %Y"))
                date_object.strftime("%B %d, %Y")
                date_range_array.append(date_object.strftime("%B %d, %Y"))

            # Compare the start date
            start_date = dt.strptime(x, "%B %d, %Y")
            iter_date = "November 18, 2019"
            end_date = dt.strptime(y, "%B %d, %Y")
        
            # Error checking to see if start day is valid
            if start_date > end_date:
                return "ERROR: Start date cannot be greater than end date."
            if start_date == end_date:
                return "ERROR: End date must be at least one day later than the start date."
 
            print()    
            print("-----Displaying information for the purchases made on or after ", x, " and before ", y, "-----")
            print()
            z = 0
            i = 0
            executed = False
            for i in range(len(date_range_array)):     
                search = transactions.find({'Timestamp': date_range_array[i]})
                for match in search:
                    results.append(match)
                    executed = True
                i += 1
                
            return results

            if executed == False:
                return "**NO TRANSACTIONS OCCURRED DURING THIS TIME RANGE**"
                
                
                
                