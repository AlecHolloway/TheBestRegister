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
    def search_database(criteria, term, startDate, endDate, transactions = transactionsAtt):

        # First, get a list of stuff between startDate and endDate
        # if nothing was entered for either, then ignore it
        # do the searches below on the list of stuff between start and end date
        if (startDate != "") and (endDate != ""):
            print("Date range selected")
            print("Start date: ", startDate)
            print("End date: ", endDate)
            i = 0.0
            print()

            # x = startDate
            # y = endDate
            
            # print list of dates within range
            start = datetime.datetime.strptime(startDate, "%B %d, %Y")
            end = datetime.datetime.strptime(endDate, "%B %d, %Y")
            date_array = \
                (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))

            date_range_array = []
            # Date of transactions within range entered
            for date_object in date_array:
                #print(date_object.strftime("%B %d, %Y"))
                date_object.strftime("%B %d, %Y")
                date_range_array.append(date_object.strftime("%B %d, %Y"))

            print()

            # Compare the start date
            start_date = dt.strptime(startDate, "%B %d, %Y")
            end_date = dt.strptime(endDate, "%B %d, %Y")
        
            # Error checking to see if start day is valid
            if start_date > end_date:
                print("ERROR: Start date cannot be greater than end date.")
                print()
                print()
                database.search_database(criteria, term, startDate, endDate)
            if start_date == end_date:
                print("ERROR: End date must be at least one day later than the start date.")
                print()
                print()
                database.search_database(criteria, term, startDate, endDate)
            print()    
            print("-----Displaying information for the purchases made on or after ", startDate, " and before ", endDate, "-----")
            print()
            z = 0
            i = 1
            executed = False
            for i in range(len(date_range_array)):     
                search = transactions.find({'Timestamp': date_range_array[i]})
                for match in search:
                    print(match)
                    executed = True
                i += 1

            if executed == False:
                print("**NO TRANSACTIONS OCCURRED DURING THIS TIME RANGE**")
                print()
                print(date_range_array)
                database.search_database(criteria, term, startDate, endDate)
            print()
            print()

        #if no date range selected        
        if criteria in ('TransactionID', 'Location', 'PaymentInfo'):
            history_array = []
            
            start = transactions.find({criteria:term})
        
            for i in start:
                
                a = 'ID:' + i['TransactionID'] 
                b = 'Items:' + str(i['Items'])         
                c = 'Timestamp:' + i['Timestamp']
                #d = ('Transaction hash:', i['this_hash'])
                e = 'Store Location:' + i['Location']        
                f = 'Transaction Cost:' + i['PaymentTotal']
                g = 'Payment Method:' + i['PaymentInfo'] 
                

                history_array.extend([ a , '\n' + b,'\n' + c,'\n' + e , '\n' + f,'\n' + g])
                
            return history_array
        
            if history_array == []:
                history_array = "No results found"
        
        elif criteria in ('Items'):
            history_array = "NOT YET IMPLEMENTED"
        
        return history_array # Stuff that will show up in '_HISTORY_'

    #Connor's search 
##    def search_database():
##        #BE CAREFUL UNCOMMENTING NEXT LINE
##        print()
##        transactions = db.transactions
##        date_range_array = []
##
##        #make classes callable
##        blockchain = Blockchain()
##        block = Block(0,0,0)
##        print()
##        print("----------Program Running----------")
##        print("Current date:", block.timestamp)
##        print()   
##
##
##        # Give choice of searching by date or transaction ID
##        answer = str(input("Would you like to search by date or by transaction ID (enter 'date' or 'id'): "))
##        print()
##        print()
##
##        print()
##        if (answer == "id"):
##            # searching the database by transaction number
##            answer = input("Enter which transaction ID you would like to display: ")
##
##            # Error checking for ID to be an int
##            while answer.isdigit() == False:
##                print("ERROR: Please enter a positive valid integer for transaction ID")
##                answer = input("Enter which transaction ID you would like to display: ")
##            ## turns x into int
##            if answer.isdigit():
##                answer = int(answer)
##
##            i = 0        
##            results = transactions.find({"_id":answer})
##            print("Displaying information for transaction ID: ", answer)
##            for x in results:
##                print(x)
##
##        elif (answer == "date"):
##            # searching by date
##            # declare variables for start and end date
##            i = 0.0
##            x = str(input("Enter the start date as Month Day, Year (Ex: November 18, 2019) **Start date is inclusive**: "))
##            y = str(input("Enter the end date as Month Day, Year (Ex: November 19, 2019) **End date is non-inclusive**: "))
##            print()
##
##            # print list of dates within range
##            start = datetime.datetime.strptime(x, "%B %d, %Y")
##            end = datetime.datetime.strptime(y, "%B %d, %Y")
##            date_array = \
##                (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))
##
##            # Date of transactions within range entered
##            for date_object in date_array:
##                #print(date_object.strftime("%B %d, %Y"))
##                date_object.strftime("%B %d, %Y")
##                date_range_array.append(date_object.strftime("%B %d, %Y"))
##
##            print()
##
##            # Compare the start date
##            start_date = dt.strptime(x, "%B %d, %Y")
##            iter_date = "November 18, 2019"
##            end_date = dt.strptime(y, "%B %d, %Y")
##        
##            # Error checking to see if start day is valid
##            if start_date > end_date:
##                print("ERROR: Start date cannot be greater than end date.")
##                print()
##                print()
##                search_database()
##            if start_date == end_date:
##                print("ERROR: End date must be at least one day later than the start date.")
##                print()
##                print()
##                search_database()
##            print()    
##            print("-----Displaying information for the purchases made on or after ", x, " and before ", y, "-----")
##            print()
##            z = 0
##            i = 0
##            executed = False
##            for i in range(len(date_range_array)):     
##                search = transactions.find({'Timestamp': date_range_array[i]})
##                for match in search:
##                    print(match)
##                    executed = True
##                i += 1
##
##            if executed == False:
##                print("**NO TRANSACTIONS OCCURRED DURING THIS TIME RANGE**")
##                print()
##                search_database()
##            print()
##            print()
##            
##        else:
##            print("ERROR: INVALID INPUT")
##            print()
##            print()
##            search_database()
##
##        print()
##        print()
##        search_database()



        #Hayden's search
##    def search(criteria, term, transactions = transactionsAtt):
##        
##        if criteria in ('TransactionID', 'Location', 'PaymentInfo'):
##            results = []
##            for x in transactions.find({criteria:term}):
##                results.append(x)
##            if results == []:
##                results = "No results found"
##        
##        elif criteria in ('Items'):
##            results = "NOT YET IMPLEMENTED"
##        
##        elif criteria in ('Timestamp'):
##            results = "NOT YET IMPLEMENTED"
##        
##        return results # Stuff that will show up in '_HISTORY_'
