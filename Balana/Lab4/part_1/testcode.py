import code
import unittest

class TestCode(unittest.TestCase):
  def testsimple(self):
    self.assertEqual(code.return_zero(),0)

if __name__=='__main__':
  unittest.main()