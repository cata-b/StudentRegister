import unittest
from Domain.Grade import Grade
from Domain.CustomErrors import InvalidParametersError

class Test_Grade(unittest.TestCase):
    def test___init__(self):
        g = Grade(1, 1, 1, 5)
        self.assertEqual(g.StudentID, 1)
        self.assertEqual(g.DisciplineID, 1)
        self.assertEqual(g.Value, 5)
        with self.assertRaises(InvalidParametersError):
            Grade("foo", 1, 1, 1)
        with self.assertRaises(InvalidParametersError):
            Grade(1, "foo", 1, 1)
        with self.assertRaises(InvalidParametersError):
            Grade(1, 1, "foo", 1)
        with self.assertRaises(InvalidParametersError):
            Grade(1, 1, 1, "foo")
        with self.assertRaises(InvalidParametersError):
            Grade(1, 1, 1, 100)
        with self.assertRaises(InvalidParametersError):
            Grade(1, 1, 1, -1)

    def test_StudentID_setter(self):
        g = Grade(1, 1, 1, 1)
        g.StudentID = 2
        self.assertEqual(g.StudentID, 2)
        with self.assertRaises(InvalidParametersError):
            g.StudentID = "foo"

    def test_DisciplineID_setter(self):
        g = Grade(1, 1, 1, 1)
        g.DisciplineID = 2
        self.assertEqual(g.DisciplineID, 2)
        with self.assertRaises(InvalidParametersError):
            g.DisciplineID = "foo"

    def test_Value_setter(self):
        g = Grade(1, 1, 1, 1)
        g.Value = 2
        self.assertEqual(g.Value, 2)
        with self.assertRaises(InvalidParametersError):
            g.Value = "foo"
        with self.assertRaises(InvalidParametersError):
            g.Value = 100

if __name__ == '__main__':
    unittest.main()
