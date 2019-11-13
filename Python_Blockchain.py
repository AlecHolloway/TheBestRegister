import datetime
import hashlib
from pygrok import Grok
import time


class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()
    store_location = "601 Critz Street Starkville, MS"

    trans_id = 0

    def __init__(self, data):
        self.data = data
        

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8') + 
        str(self.trans_id).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\nTimestamp: " + str(self.timestamp) + "\nTransaction ID: " + str(self.trans_id) + "\nStore Location: " + str(self.store_location) + "\n--------------"

class Blockchain:

    diff = 20
    maxNonce = 2**32
    target = 2 ** (256-diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):
        block.trans_id = self.block.trans_id + 1
        
        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next
        print("---transaction added---")

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1

def main():
    block = Block(0)
    blockchain = Blockchain()
    print("Current time:", block.timestamp)

    #add data to the blockchain
    blockchain.add(Block("Apples : $4.45"))
    #time.sleep(1)
    blockchain.add(Block("Oranges : $6.54"))
    #time.sleep(1)
    blockchain.add(Block("Pairs: $2.23"))


    #Give choice of searching by date or transaction ID
    answer = str(input("Would you like to search by date or by transaction ID (enter 'date' or 'id'): "))

    if (answer == "id"):
        #searching by block number
        x = int(input("Enter which transaction ID you would like to display: "))

        i = 0
        #Print the selected block
        while i < x:
            blockchain.head = blockchain.head.next
            i += 1
        print("Displaying information for the number ", x, " block: ")
        print(blockchain.head)

    elif (answer == "date"):
        #searching by date
        #declare variables for start and end date
        i = 0.0
        x = str(input("Enter the start date (yyyy-mm-dd): "))
        y = str(input("Enter the end date (yyyy-mm-dd): "))
        print()

        
        #print list of dates within range
        start = datetime.datetime.strptime(x, "%Y-%m-%d")
        end = datetime.datetime.strptime(y, "%Y-%m-%d")
        date_array = \
            (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))
        
        #Date of transactions within range entered
        for date_object in date_array:
            print(date_object.strftime("%Y-%m-%d"))
            
        #Change blockchain timestamps into strings
        while blockchain.head != None:
            start_date_str = str(blockchain.head.timestamp)
            start_date = start_date_str[:10]
            print("Timestamps as strings: ", start_date)
            #move to next block
            blockchain.head = blockchain.head.next

            
            #print("Printing each block timestamp", blockchain.head.timestamp)
        
            
        #start_date_str = str(block.timestamp)
        #start_date = start_date_str[:10]
        #print("Start date as a string: ", start_date)

        
        #Print entire blockchain
        print()
        print("PRINTING THE ENTIRE BLOCKCHAIN")
        print()
        while blockchain.head != None:
            print(blockchain.head)
            blockchain.head = blockchain.head.next



        print("Displaying information for the purchases made on or after ", x, " and before ", y)

##    #Printing blocks within date range
##    for date_object in date_array:
##        print(date_object.strftime("%Y-%m-%d"))
##        while start != self.timestamp
    


    
#Print the blocks based on date of purchase
    #Move to starting date block
##    while i < x:
##        blockchain.head = blockchain.head.next
##        i += 1


    #Print blocks until end date reached
##    while i < y:
##        print(blockchain.head)
##        blockchain.head = blockchain.head.next



    #Print entire blockchain
##    while blockchain.head != None:
##        print(blockchain.head)
##        blockchain.head = blockchain.head.next
    else:
        print("Error: INVALID INPUT")
        print()
        print()
        main()
        
    print()
    print()
    main()
main()



#Reference used: https://github.com/howCodeORG/Simple-Python-Blockchain/blob/master/blockchain.py
