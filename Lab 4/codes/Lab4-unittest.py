import unittest
import oxo_gui_complete

class gameTest(unittest.TestCase):
    def testSample(oxo_gui_complete):
        oxo_gui_complete.assertEqual(oxo_gui_complete.get_winner(), None)

if __name__ == '__main__':
    unittest.main()
"""
Author: Pelagio, Jansen Andrey G. Pelagio
Date: 2023-10-16
Description: A python program that tests the code similar to a simulation of a game of
Tic Tac Toe.
"""