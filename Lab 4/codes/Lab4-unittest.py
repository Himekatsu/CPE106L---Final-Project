import unittest
import oxo_gui_complete

class gameTest(unittest.TestCase):
    def testSample(oxo_gui_complete):
        oxo_gui_complete.assertEqual(1+1,2)

if __name__ == '__main__':
    unittest.main()