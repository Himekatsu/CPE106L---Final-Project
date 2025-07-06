from pymongo import MongoClient
import pprint
import re

# client = MongoClient(host='localhost', port=27017)
client = MongoClient('mongodb://localhost:27017/')
db = client["chinook"]
collection = db["customers"]
doc1 = collection.find_one()
print(doc1)

client.close()