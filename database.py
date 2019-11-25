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

# For blockchain functionality
import datetime
from datetime import datetime as dt

import hashlib

# For database functionality
import pymongo

# For storing objects in MongoDB
from bson.binary import Binary
import pickle

# For sleeping
import time

client = pymongo.MongoClient("mongodb+srv://chapiiin:password20@cluster0-6dsmr.gcp.mongodb.net/test?retryWrites=true&w=majority")
storage = client.TestTBR


class Block:
    blockNo = 0
    data = {}
    next_hash = None
    this_hash = None
    nonce = 0
    previous_hash = None
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%B %d, %Y")
    
    def __init__(self, data):
        self.data = data
        self.this_hash = self.data['this_hash']

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.blockNo).encode('utf-8')
        )
        
        new_hash = h.hexdigest()
        self.this_hash = new_hash
        self.data['this_hash'] = self.this_hash
        
        return new_hash

    def __str__(self):
        return (
            "Block Hash: " + str(self.hash()) +
            "\nBlockNo: " + str(self.blockNo) +
            "\nBlock Data: " + str(self.data) +
            "\nHashes: " + str(self.nonce) +
            "\n--------------"
        )


class Blockchain:
    transactionsAtt = storage.transactions
    diff = 20
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)

    block = Block({'title':'Genesis','this_hash':'START'})
    dummy = head = block
    
    def __init__(self, block = block):
        self.block = block
    
    def add(self, block, transactions = transactionsAtt):        
        
        self.block.next_hash = block.hash()
        block.previous_hash = self.block.this_hash
        block.blockNo = self.block.blockNo + 1
        
        transactions.update_one({'this_hash':block.previous_hash},
                                {'$set':{'next_hash':self.block.next_hash}})
        
        self.block.data['next_hash'] = self.block.next_hash
        block.data['previous_hash'] = block.previous_hash
        block.data['blockNo'] = block.blockNo
        
        block.data['TransactionID'] = str(block.data['blockNo'])
        
        self.block = block

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1


class database:
    transactionsAtt = storage.transactions
    
    # Function to delete all data from the database
    def empty_database(transactions = transactionsAtt):
        print("Emptying database")
        result = transactions.delete_many({})
        print("\nSleeping\n")
        time.sleep(1000)

    # Function to add entire blockchain to database
    def update_database(data, transactions = transactionsAtt):
            
        # If database (collection) is empty, add a new blockchain object
        if transactions.count() == 0:
            result = "\n\nDATABASE IS EMPTY, ADDING NEW BLOCKCHAIN\n\n"
            print(result)
            
            blockchainEntryNew = {}
            
            blockchainObjectNew = Blockchain()
            
            # Convert blockchain into binary and store it
            blockchainBytesNew = pickle.dumps(blockchainObjectNew)
            blockchainEntryNew['title'] = 'blockchain'
            blockchainEntryNew['data'] = Binary(blockchainBytesNew)
            blockchainEntryNew['edits'] = 0
            transactions.insert_one(blockchainEntryNew)

        # Get blockchain
        blockchainRetrieved = transactions.find_one({'title': 'blockchain'})
        blockchain = pickle.loads(blockchainRetrieved['data'])
        
        # Add block
        block = Block(data)
        blockchain.add(block)
        
        # Add data entry
        transactions.insert_one(data)
        
        # Convert blockchain back into binary and update its entry in the database
        blockchainBytes = pickle.dumps(blockchain)
        blockchainBinary = Binary(blockchainBytes)
        transactions.update_one({'title':'blockchain'},{'$set':{'data':blockchainBinary}})
        transactions.update_one({'title':'blockchain'},{'$set':{'edits':blockchainRetrieved['edits']+1}})


    #Combined search attempt
    def search_database(criteria, term, startDate, transactions = transactionsAtt):
        history_array = []
        dateSelected = False
        # First, get a list of stuff between startDate and endDate
        # if nothing was entered for either, then ignore it
        # do the searches below on the list of stuff between start and end date
        if (startDate != ""):
            print("Date search selected")
            dateSelected = True
            
            print("Start date: ", startDate)
            #print("End date: ", endDate)
            i = 0.0
            print()

            
##            # print list of dates within range
##            try:
##                start = datetime.datetime.strptime(startDate, "%B %d, %Y")
##                end = datetime.datetime.strptime(endDate, "%B %d, %Y")
##            except:
##                print("Date must be entered in correct format. (Ex: November 25, 2019)")
##                history_array.extend(["Date must be entered in correct format. (Ex: November 25, 2019)"])
##                return history_array
##                
##                
##            date_array = \
##                (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))
##
##            date_range_array = []
##            # Date of transactions within range entered
##            for date_object in date_array:
##                print(date_object.strftime("%B %d, %Y"))
##                date_object.strftime("%B %d, %Y")
##                date_range_array.append(date_object.strftime("%B %d, %Y"))
##
##            print()
##            print("Date range array: ", date_range_array)
##
##            # Compare the start date
##            start_date = dt.strptime(startDate, "%B %d, %Y")
##            #end_date = dt.strptime(endDate, "%B %d, %Y")
##        
##            # Error checking to see if start day is valid
##            if start_date > end_date:
##                print("ERROR: Start date cannot be greater than end date.")
##                print()
##                print()
##                history_array.extend(["ERROR: Start date cannot be greater than end date."])
##                return history_array
##                database.search_database(criteria, term, startDate)
##            if start_date == end_date:
##                print("ERROR: End date must be at least one day later than the start date.")
##                print()
##                print()
##                history_array.extend(["ERROR: End date must be at least one day later than the start date."])
##                return history_array
##                database.search_database(criteria, term, startDate)
##            print()    
##            print("-----Displaying information for the purchases made on or after ", startDate, " and before ", endDate, "-----")
##            print()

            #Find the last transaction
            transactionsAtt = storage.transactions
            last_doc = transactionsAtt.find().sort('TransactionID', pymongo.DESCENDING).limit(1)

            #Find the last transaction ID
            for x in last_doc:
                lastTransactionID = x['TransactionID']

            lastTransactionID = int(lastTransactionID)
            
            z = 0
            i = 1
            dateMatch = []
            history_array = []
            executed = False
                 
            start = transactions.find({'Timestamp': startDate})
            for match in start:
                print(match)
                print("--date match found--")
                a = 'ID:' + match['TransactionID'] + '\n'
                b = 'Items:' + str(match['Items']) + '\n'        
                c = 'Timestamp:' + match['Timestamp'] + '\n'
                #d = ('Transaction hash:', i['this_hash'])
                e = 'Store Location:' + match['Location'] + '\n'        
                f = 'Transaction Cost:' + match['PaymentTotal'] + '\n'
                g = 'Payment Method:' + match['PaymentInfo'] + '\n' + '\n'

                history_array.extend([a,b,c,e,f,g])
                executed = True
                    
            return history_array
                
            

#############################################################################
            
            if history_array == []:
                history_array.extend(["No results found"])
                return history_array
                
            
################################################################################3
            print("date match array:", dateMatch)
            return dateMatch
        
            if executed == False:
                print("**NO TRANSACTIONS OCCURRED DURING THIS TIME RANGE**")
                print()
                history_array.extend(["**NO TRANSACTIONS OCCURRED DURING THIS TIME RANGE**"])
                
                return history_array
                database.search_database(criteria, term, startDate, endDate)
            print()
            print()
        # Return result if no filter is selected but start/end date is given
        if (term == ""):
            history_array.extend(["Please enter a filter to search by."])
            return history_array


        #if date range selected
##        if (criteria in ('TransactionID', 'Location', 'PaymentInfo')) and (dateSelected == True):
##
##            #Find the last transaction
##            transactionsAtt = storage.transactions
##            last_doc = transactionsAtt.find().sort('TransactionID', pymongo.DESCENDING).limit(1)
##
##            #Find the last transaction ID
##            for x in last_doc:
##                lastTransactionID = x['TransactionID']
##                
##            dateMatches = []
##            history_array = []
##            print()
##            print("--DATE RANGE SELECTED WITH FILTER ADDED--")
##            print(date_range_array)
##            #transactions with matching criteria
##            start = transactions.find({criteria:term})
##            #transactions with matching date
##            for x in range(len(5)):
##                dateMatch = transactions.find({"Timestamp":date_range_array[i]})
##                dateMatches.extend([dateMatch])
##                
##            print("dateMatches array: ", dateMatches)
##        
##            for i in start:
##                
##                a = 'ID:' + i['TransactionID'] + '\n'
##                b = 'Items:' + str(i['Items']) + '\n'        
##                c = 'Timestamp:' + i['Timestamp'] + '\n'
##                #d = ('Transaction hash:', i['this_hash'])
##                e = 'Store Location:' + i['Location'] + '\n'        
##                f = 'Transaction Cost:' + i['PaymentTotal'] + '\n'
##                g = 'Payment Method:' + i['PaymentInfo'] + '\n' + '\n'
##                
##
##                history_array.extend([a,b,c,e,f,g])
##                print("History array: ")
##                print(history_array)
##
##
##            if history_array == []:
##                history_array.extend(["No results found"])
##                return history_array
##                
##            return history_array

        
        #if no date range selected        
        if criteria in ('TransactionID', 'Location', 'PaymentInfo'):
            history_array = []
            
            start = transactions.find({criteria:term})
        
            for i in start:
                
                a = 'ID:' + i['TransactionID'] + '\n'
                b = 'Items:' + str(i['Items']) + '\n'        
                c = 'Timestamp:' + i['Timestamp'] + '\n'
                #d = ('Transaction hash:', i['this_hash'])
                e = 'Store Location:' + i['Location'] + '\n'        
                f = 'Transaction Cost:' + i['PaymentTotal'] + '\n'
                g = 'Payment Method:' + i['PaymentInfo'] + '\n' + '\n'
                

                history_array.extend([a,b,c,e,f,g])
                print("History array: ")
                print(history_array)


            if history_array == []:
                history_array.extend(["No results found"])
                return history_array
                
            return history_array
    

        else:
            history_array.extend(["TRANSACTION DOES NOT EXIST"])            
            return history_array # Stuff that will show up in '_HISTORY_'
