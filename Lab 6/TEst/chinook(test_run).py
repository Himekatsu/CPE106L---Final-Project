from pymongo import MongoClient
import pprint
import re

# client = MongoClient(host="localhost", port=27017)
client = MongoClient("mongodb://localhost:27017/")

# Get reference to 'chinook' database
db = client["chinook"]

# Get a reference to the 'customers' collection
customers_collection = db["customers"]
# print(customers_collection)

#print first document
doc1 = customers_collection.find_one()
print(doc1)

client.close()
