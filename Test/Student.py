import unittest
from Domain.Student import Student
from Domain.CustomErrors import InvalidParametersError

class Test_Student(unittest.TestCase):
    def test___init__(self):
        s = Student(1, "foo")
        self.assertEqual(s.ID, 1)
        self.assertEqual(s.Name, "foo")
        with self.assertRaises(InvalidParametersError):
            Student("foo", 1)
        with self.assertRaises(InvalidParametersError):
            Student(1, 2)

    def test_setter(self):
        s = Student(1, "1")
        s.Name = "2"
        self.assertEqual(s.Name, "2")
        with self.assertRaises(InvalidParametersError):
            s.Name = 1
    def test___str__(self):
        s = Student(1, "1")
        self.assertEqual(str(s), "ID: 1, Name: 1")
if __name__ == '__main__':
    unittest.main()
