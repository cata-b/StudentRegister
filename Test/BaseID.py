import unittest
from Domain.BaseID import BaseID
from Domain.CustomErrors import InvalidParametersError

class Test_BaseID(unittest.TestCase):
    def test___init__(self):
        x = BaseID(10)
        self.assertEqual(x.ID, 10)
        with self.assertRaises(InvalidParametersError):
            BaseID("foo")

    def test_setter(self):
        x = BaseID(0)
        x.ID = 1
        with self.assertRaises(InvalidParametersError):
            x.ID = "foo"
        

if __name__ == '__main__':
    unittest.main()

