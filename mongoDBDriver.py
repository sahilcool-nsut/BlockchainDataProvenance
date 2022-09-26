from pymongo import MongoClient

def insertOne(data):
    client = MongoClient("mongodb+srv://dbUser:test@blockchaintry.uyultsy.mongodb.net/?retryWrites=true&w=majority")
    # Access database
    mydatabase = client['firstCollection']
    
    # Access collection of the database
    print("started query")
    largestCollection=mydatabase['temporaryCollection']
    res = largestCollection.insert_one(data)
    print(res)
    print("added data in mongodb")

