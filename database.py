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
    timestamp = datetime.datetime.now()
    
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

    def search(criteria, term, transactions = transactionsAtt):
        
        if criteria in ('TransactionID', 'Location', 'PaymentInfo'):
            results = []
            for x in transactions.find({criteria:term}):
                results.append(x)
            if results == []:
                results = "No results found"
        
        elif criteria in ('Items'):
            results = "NOT YET IMPLEMENTED"
        
        elif criteria in ('Timestamp'):
            results = "NOT YET IMPLEMENTED"
        
        return results # Stuff that will show up in '_HISTORY_'