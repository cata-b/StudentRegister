import unittest
from Domain.Discipline import Discipline
from Domain.CustomErrors import InvalidParametersError

class Test_Discipline(unittest.TestCase):
    def test___init__(self):
        d = Discipline(1, "foo")
        self.assertEqual(d.ID, 1)
        self.assertEqual(d.Name, "foo")
        with self.assertRaises(InvalidParametersError):
            Discipline("foo", 1)
        with self.assertRaises(InvalidParametersError):
            Discipline(1, 2)

    def test_setter(self):
        d = Discipline(1, "1")
        d.Name = "2"
        self.assertEqual(d.Name, "2")
        with self.assertRaises(InvalidParametersError):
            d.Name = 1
    def test___str__(self):
        d = Discipline(1, "1")
        self.assertEqual(str(d), "ID: 1, Name: 1")
if __name__ == '__main__':
    unittest.main()
