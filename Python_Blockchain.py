import datetime
import hashlib
from pygrok import Grok
import time
from datetime import datetime as dt
import collections


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
    head_start = head
    

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
    counter = 0
    
    #add data to the blockchain
    blockchain.add(Block("Apples : $4.45"))
    counter += 1
    #time.sleep(1)
    blockchain.add(Block("Oranges : $6.54"))
    counter += 1
    #time.sleep(1)
    blockchain.add(Block("Pairs: $2.23"))
    counter += 1
    
    print("Counter value after 3 transactions: ", counter)

    #Give choice of searching by date or transaction ID
    answer = str(input("Would you like to search by date or by transaction ID (enter 'date' or 'id'): "))
    print()
    print()


    print()
    if (answer == "id"):
        #searching by block number
        x = int(input("Enter which transaction ID you would like to display: "))

        #Error checking for ID to be an int
        
        i = 0
        #Print the selected block        
        if x > counter:
            print("ERROR: out of range")
            print()
            main()
            
        while i < x:
            blockchain.head = blockchain.head.next
            i += 1
            print()
        print("Displaying information for transaction ID: ", x)
        print()
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
##        while blockchain.head != None:
##            date_str = str(blockchain.head.timestamp)
##            date = date_str[:10]
##            print("Timestamps as strings: ", date)
##            #move to next block
##            blockchain.head = blockchain.head.next

        date_str = str(blockchain.head.timestamp)
        date = date_str[:10]
            #print("Printing each block timestamp", blockchain.head.timestamp)
    
        
        #Compare the start date
        start_date = dt.strptime(x, "%Y-%m-%d")
        iter_date = dt.strptime(date, "%Y-%m-%d")
        end_date = dt.strptime(y, "%Y-%m-%d")


        #Error checking to see if start day is valid
        if start_date > end_date:
            print("ERROR: Start date cannot be greater than end date.")
            print()
            print()
            main()
            
            
        #Search for the first transaction within the selected range
        while iter_date < start_date:
            print()
            print("Comparing start date to iteration.")
            print("Start date: ", start_date, "Iteration date: ", date)
            blockchain.head_start = blockchain.head_start.next

        #Display the transactions withing the selected range
        n = 0
        while iter_date <= end_date:
            print()
            print("Comparing iteration to end date.")
            print(blockchain.head_start.timestamp, " is within the range.")
            print("Iteration date: ",iter_date, "End date: ", end_date)
            print(blockchain.head_start)
            blockchain.head_start = blockchain.head_start.next
            n += 1
            if n >= 4:
                break

            
        #add data to the blockchain
        blockchain.add(Block("Cucumbers : $5.69"))
        
##        #Print entire blockchain
##        print()
##        print("PRINTING THE ENTIRE BLOCKCHAIN")
##        print()
##        while blockchain.head_start != None:
##            print(blockchain.head_start)
##            blockchain.head_start = blockchain.head_start.next




        print("Displaying information for the purchases made on or after ", x, " and before ", y)

##    #Printing blocks within date range
##    for date_object in date_array:
##        print(date_object.strftime("%Y-%m-%d"))
##        while start != self.timestamp
    




    #Print entire blockchain
##    while blockchain.head != None:
##        print(blockchain.head)
##        blockchain.head = blockchain.head.next


    
    else:
        print("ERROR: INVALID INPUT")
        print()
        print()
        main()
        
    print()
    print()
    main()
main()



#Reference used: https://github.com/howCodeORG/Simple-Python-Blockchain/blob/master/blockchain.py
#Reference used: https://stackoverflow.com/questions/20365854/comparing-two-date-strings-in-python
