import datetime
import hashlib
from pygrok import Grok
import time
from datetime import datetime as dt

#imports for database
import pymongo
#from pymongo import MongoClient
#client = MongoClient()

import motor

client = pymongo.MongoClient("mongodb+srv://chapiiin:password20@cluster0-6dsmr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.TBR

# Database imports
# from bigchaindb_driver import BigchainDB
# from bigchaindb_driver.crypto import generate_keypair


class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%B %d, %Y")
    store_location = "601 Critz Street Starkville, MS"

    tbr_dict = {
        }

    #trans_id = 0
    _id = 0
    
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
            str(self._id).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nTransaction ID: " + str(self.blockNo) + "\nBlock Data: " + str(
            self.data) + "\nTimestamp: " + str(
            self.timestamp) + "\nTransaction ID: " + str(self._id) + "\nStore Location: " + str(
            self.store_location) + "\n--------------"


class Blockchain:
    diff = 20
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)

    block = Block("Genesis")
    dummy = head = block
    head_start = head
    head_start2 = head

    def add(self, block):
        #Counter variable
        #block.counter = self.block.counter + 1
        
        block._id = self.block._id + 1

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
    #hard coded counter
    counter = 4
    
    print()
    transactions = db.transactions
    date_range_array = []
    

    #Finds all posts from DB
##    print()
##    print()
##    print("---Print all contents of the database---")
##    results = transactions.find({})
##    #iterate over the data to print to screen
##    for x in results:
##        print(x)
            

##    print("Sleeping")
##    time.sleep(120)
    

    block = Block(0)
    blockchain = Blockchain()
    print()
    print("----------Program Running----------")
    print("Current date:", block.timestamp)
    print()
    
    #counter = 0

##    # add data to the blockchain
##    blockchain.add(Block("Apples : $4.45"))
##    
##    # time.sleep(1)
##    blockchain.add(Block("Oranges : $6.54"))
##    
##    # time.sleep(1)
##    blockchain.add(Block("Pairs: $2.23"))
    

    tbr_dict = block.tbr_dict
    transactions = db.transactions


##    #upadating dictionary and pushing transactions to database
##    while blockchain.head_start2 != None:
##        print("ADDING TO DICTIONARY")
##        block.tbr_dict.update({"_id":blockchain.head_start2._id})
##        block.tbr_dict.update({"Items purchased":blockchain.head_start2.data})
##        block.tbr_dict.update({"Timestamp":blockchain.head_start2.timestamp})
##        block.tbr_dict.update({"Transaction hash":blockchain.head_start2.hash()})
##        block.tbr_dict.update({"Store Location":blockchain.head_start2.store_location})
##
##
##        result2 = transactions.insert_one(block.tbr_dict)
##        blockchain.head_start2 = blockchain.head_start2.next
        
    #print("New counter value after 3 transactions: ", blockchain.block.counter)


    # Give choice of searching by date or transaction ID
    answer = str(input("Would you like to search by date or by transaction ID (enter 'date' or 'id'): "))
    print()
    print()

    print()
    if (answer == "id"):
        # searching the database by transaction number
        answer = input("Enter which transaction ID you would like to display: ")

        # Error checking for ID to be an int
        while answer.isdigit() == False:
            print("ERROR please enter an int for ID")
            answer = input("Enter which transaction ID you would like to display: ")
        ## turns x into int
        if answer.isdigit():
            answer = int(answer)

        i = 0
        # Print the selected block
        #if x > blockchain.block.counter:
        #    print("ERROR: out of range")
        #    print()
        #    main()

        
        results = transactions.find({"_id":answer})
        print("Displaying information for transaction ID: ", answer)
        for x in results:
            print(x)

    elif (answer == "date"):
        # searching by date
        # declare variables for start and end date
        i = 0.0
        x = str(input("Enter the start date as Month Day, Year (Ex: November 18, 2019): "))
        y = str(input("Enter the end date as Month Day, Year (Ex: November 19, 2019) **End date is non-inclusive**: "))
        print()

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

        print()

#prints dates within user selected date range
##        print("Printing date_range_array")
##        z = 0
##        i = 0
##        for z in range(len(date_range_array)):
##            print(date_range_array[i])
##            i += 1

        
                
        # print("Printing each block timestamp", blockchain.head.timestamp)

        # Compare the start date
        start_date = dt.strptime(x, "%B %d, %Y")
        iter_date = "November 18, 2019"
        end_date = dt.strptime(y, "%B %d, %Y")
    
        #truncate start date string
        #start_date = start_date[:10]
        
        # Error checking to see if start day is valid
        if start_date > end_date:
            print("ERROR: Start date cannot be greater than end date.")
            print()
            print()
            main()
        if start_date == end_date:
            print("ERROR: End date must be at least one day later than the start date.")
            print()
            print()
            main()
        # Search for the first transaction within the selected range
        #while iter_date < start_date:
        #    print()
 
        print()    
        print("-----Displaying information for the purchases made on or after ", x, " and before ", y, "-----")
        print()
        z = 0
        i = 0
        for i in range(len(date_range_array)):     
            search = transactions.find({'Timestamp': date_range_array[i]})
            for match in search:
                print(match)
            i += 1
        print()
        print()
        

# add data to the blockchain
##        blockchain.add(Block("Cucumbers : $5.69"))

        ##        #Print entire blockchain
        ##        print()
        ##        print("PRINTING THE ENTIRE BLOCKCHAIN")
        ##        print()
        ##        while blockchain.head_start != None:
        ##            print(blockchain.head_start)
        ##            blockchain.head_start = blockchain.head_start.next

# Print entire blockchain
    ##    while blockchain.head != None:
    ##        print(blockchain.head)
    ##        blockchain.head = blockchain.head.next


            
#Retrieving data from the DB
        #Finds one post from DB
##        bills_post = posts.find_one({'author': 'Bill'})
##        print(bills_post)
##        #Finds multiple posts from DB
##        scotts_posts = posts.find({'author': 'Scott'})
##        print(scotts_posts)
##            #iterate over the data to print to screen
##        for post in scotts_posts:
##            print(post)
        
    else:
        print("ERROR: INVALID INPUT")
        print()
        print()
        main()

    print()
    print()
    main()


main()

# Reference used: https://github.com/howCodeORG/Simple-Python-Blockchain/blob/master/blockchain.py
# Reference used: https://stackoverflow.com/questions/20365854/comparing-two-date-strings-in-python
# Reference used: https://thispointer.com/python-how-to-convert-datetime-object-to-string-using-datetime-strftime/
# Instructions to access database: https://realpython.com/introduction-to-mongodb-and-python/

