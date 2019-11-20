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
    data = None
    next = None
    hash = None
    nonce = 0
    cost = 0
    payment = None
    previous_hash = 0x0
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%B %d, %Y")
    store_location = "601 Critz Street Starkville, MS"

    tbr_dict = {
        }

    #trans_id = 0
    _id = 0
    
    def __init__(self, data, cost, payment):
        self.data = data
        self.cost = cost
        self.payment = payment

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.blockNo).encode('utf-8') +
            str(self._id).encode('utf-8') +
            str(self.payment).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nTransaction ID: " + str(self.blockNo) + "\nBlock Data: " + str(
            self.data) + "\nTimestamp: " + str(
            self.timestamp) + "\nTransaction ID: " + str(self._id) + "\nStore Location: " + str(
            self.store_location) + "\nCost: " + int(self.cost) + "\nPayment: " + str(self.payment) + "\n--------------"


class Blockchain:
    diff = 20
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)

    block = Block("Genesis", 0, 0)
    dummy = head = block
    head_start = head
    head_start2 = head
    head_start3 = head
    

    def add(self, block):        
        block._id = self.block._id + 1

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        
        self.block.next = block
        self.block = self.block.next

        #print("---transaction added---")

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1
            


class database: 
    block = Block(0, 0, 0)
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
    def update_database(counter, items, cost, payment):   
            blockchain = Blockchain()
            block = Block(0,0, '')
            tbr_dict = block.tbr_dict
            transactions = db.transactions
            #add data to the blockchain
            #blockchain.add(Block("Apples : $4.45"))
            #blockchain.add(Block("Oranges : $6.54"))
            #blockchain.add(Block("Pairs: $2.23"))
            #blockchain.add(Block("Bananas: $3.57"))
            

            #Find the last transaction
            last_doc = transactions.find().sort('_id', pymongo.DESCENDING).limit(1)
            #print("Last doc: ", last_doc)

            #Find the last transaction ID
            for x in last_doc:
                print("Last transaction: ", x)
            last_id = x["_id"]
            #print("Last ID: ", last_id)

            for i in range(last_id):
            #    print(i, " non-existent block added")
                blockchain.add(Block("Null data", 0))

            #print("blockchain head data before: ", blockchain.head_start2.data)
            #updating dictionary and pushing transactions to database
            while blockchain.head_start2._id != last_id:
            #    print("--MOVING HEAD TO LAST BLOCK IN BLOCKCHAIN--")
            #    print("Blockchain head id during: ", blockchain.head_start2._id)
            #    print("Last id: ", last_id)
            #    print("blockchain head data during: ", blockchain.head_start2.data)
                blockchain.head_start2 = blockchain.head_start2.next
                print()
            #print("Blockchain head id after: ", blockchain.head_start2._id)
            #print("Blockchain head data after loop: ", blockchain.head_start2.data)
            #print("Last id: ", last_id)    
            
        
            #add new transaction to blockchain
            blockchain.add(Block(items,cost,payment))
            #print("Blockchain head data after adding trans: ", blockchain.head_start2.data)

            #move to new transaction
            while blockchain.head_start3._id != last_id + 1:
                blockchain.head_start3 = blockchain.head_start3.next

            #print("Blockchain head data after new head loop: ", blockchain.head_start3.data)
            #update dictionary with new transaction
            print("-ADDING TO DATABASE-")
            block.tbr_dict.update({"_id":blockchain.head_start3._id})
            print("Data being added: ", blockchain.head_start3.data)
            block.tbr_dict.update({"Items purchased":blockchain.head_start3.data})
            block.tbr_dict.update({"Timestamp":blockchain.head_start3.timestamp})
            block.tbr_dict.update({"Transaction hash":blockchain.head_start3.hash()})
            block.tbr_dict.update({"Store Location":blockchain.head_start3.store_location})
            block.tbr_dict.update({"Cost":blockchain.head_start3.cost})
            block.tbr_dict.update({"Cost":blockchain.head_start3.payment})
            counter += 1
            #push transaction to database
            result2 = transactions.insert_one(block.tbr_dict)
                
            #print("Counter value: ", counter)
        #function call to update the database
        #update_database(-1)

        #temporary counter
           ##counter = 4
class search: 
    def search():
        #BE CAREFUL UNCOMMENTING NEXT LINE
    #####empty_database()

        print()
        transactions = db.transactions
        date_range_array = []
    
        #make classes callable
        block = Block(0)
        blockchain = Blockchain()
        print()
        print("----------Program Running----------")
        print("Current date:", block.timestamp)
        print()   

    



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
                print("ERROR: Please enter a positive valid integer for transaction ID")
                answer = input("Enter which transaction ID you would like to display: ")
            ## turns x into int
            if answer.isdigit():
                answer = int(answer)

            i = 0
            # Error checking for ID to be within valid range
##            if answer > counter:
##                print("ERROR: Transaction ID out of range")
##                print(counter, " is not a valid transaction ID")
##                print()
##                main()

        
            results = transactions.find({"_id":answer})
            print("Displaying information for transaction ID: ", answer)
            for x in results:
                print(x)

        elif (answer == "date"):
            # searching by date
            # declare variables for start and end date
            i = 0.0
            x = str(input("Enter the start date as Month Day, Year (Ex: November 18, 2019) **Start date is inclusive**: "))
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
                #search()
            if start_date == end_date:
                print("ERROR: End date must be at least one day later than the start date.")
                print()
                print()
                #search()
            # Search for the first transaction within the selected range
            #while iter_date < start_date:
            #    print()
 
            print()    
            print("-----Displaying information for the purchases made on or after ", x, " and before ", y, "-----")
            print()
            z = 0
            i = 0
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


    #Prints all posts from DB
    ##    print()
    ##    print()
    ##    print("---Print all contents of the database---")
    ##    results = transactions.find({})
    ##    #iterate over the data to print to screen
    ##    for x in results:
    ##        print(x)
        
        else:
            print("ERROR: INVALID INPUT")
            print()
            print()
            #search()

        print()
        print()
        #search()


    ##main()

    # Reference used: https://github.com/howCodeORG/Simple-Python-Blockchain/blob/master/blockchain.py
    # Reference used: https://stackoverflow.com/questions/20365854/comparing-two-date-strings-in-python
    # Reference used: https://thispointer.com/python-how-to-convert-datetime-object-to-string-using-datetime-strftime/
    # Instructions to access database: https://realpython.com/introduction-to-mongodb-and-python/hon/