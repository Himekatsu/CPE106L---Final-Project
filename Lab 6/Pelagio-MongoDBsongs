from pymongo import MongoClient

import pprint
import re

def printTrack(db):
    tracks_collection = db["tracks"]
    doc1 = tracks_collection.find_one()
    print(doc1)

def printAlbum(db):
    album_collection = db["albums"]
    doc1 = album_collection.find_one()
    print(doc1)

def printArtist(db):
    artist_collection = db["artists"]
    doc1 = artist_collection.find_one()
    print(doc1)
    
def main():
# client = MongoClient(host="localhost", port=27017)
    client = MongoClient("mongodb://localhost:27017/")
# Get reference to 'chinook' database
    db = client["Lab6Act"]
    printTrack(db)
    printAlbum(db)
    printArtist(db)
    client.close()

if __name__ == "__main__":
    main()