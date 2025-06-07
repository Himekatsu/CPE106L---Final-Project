import unittest 
import os
import sqlite3


class testDB(unittest.TestCase):
    def setUp(self):
        url = os.getenv('chinook.db')                  
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:            
            self.skipTest("No databasee connection set. Error {e}")



def circle_area(r):
    return pi * (r**2)

radii = [2, 0, -3, 2 + 5j, True, "radius"]
message = "area of circles with r = {radius} is {area}"

def main():
    for radius in radii:
        print(message.format(radius))


if __name__ == '__main__': 
	unittest.main() 
