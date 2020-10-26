import unittest
from Domain.BaseIDList import BaseIDList
from Domain.CustomErrors import *
from Domain.BaseID import BaseID
from Domain.Student import Student

class Test_BaseIDList(unittest.TestCase):
    def test___init__(self):
        x = BaseIDList()
        self.assertEqual(x.Length(), 0)
        self.assertEqual(x.Length(True), 0)
        self.assertEqual(x.GetSafeKey(), 1)
        self.assertEqual(x.Length(), 0)
        self.assertEqual(x.Length(True), 0)
        with self.assertRaises(InvalidParametersError):
            x.HasKey("foo")
    
    def test__Add_Remove_Update_get_undo_redo(self):
        x = BaseIDList()
        x.AddItems([BaseID(1)])
        x.SetQueryOptions(None, None, None, None, False)
        self.assertEqual(x[1].ID, 1)
        x.Undo()
        self.assertEqual(x.Length(), 0)
        self.assertEqual(x.Length(True), 0)
        x.Redo()
        with self.assertRaises(NoMoreStepsError):
            x.Redo()
        self.assertEqual(x.Length(), 1)
        self.assertEqual(x.Length(True), 1)
        x.UpdateItem(1, BaseID(2))
        with self.assertRaises(InvalidParametersError):
            x.UpdateItem(1, 1)
        self.assertEqual(x.Length(), 1)
        self.assertEqual(x.Length(True), 1)
        self.assertEqual(x[1].ID, 1) # ID is never updated
        self.assertEqual(x[0, True].ID, 1)
        x.Undo()
        x.Undo()
        self.assertEqual(x.Length(), 0)
        self.assertEqual(x.Length(True), 0)
        with self.assertRaises(NoMoreStepsError):
            x.Undo()
        x = BaseIDList()
        x.AddItems([BaseID(1)])
        with self.assertRaises(IDExistsError):
            x.AddItems([BaseID(1)])
        x = BaseIDList()
        x.AddItems([BaseID(1)])
        with self.assertRaises(InvalidParametersError):
            x.AddItems([Student(2, "Name")])
        x = BaseIDList()
        x.AddItems([BaseID(1)])
        with self.assertRaises(InvalidParametersError):
            x.AddItems([1])
        x = BaseIDList()
        x.AddItems([BaseID(1)])
        x.SetQueryOptions('ID', 1, True, None, False)
        self.assertEqual(x[0, True].ID, 1)
        x.RemoveItems([1])
        self.assertEqual(x.Length(), 0)
        x.Undo()
        self.assertEqual(x.Length(), 1)
        with self.assertRaises(InvalidParametersError):
            x.SetQueryOptions(1, 1, 1, 1, 1)

    def test_Querying(self):
        l = BaseIDList()
        l.AddItems ( 
            [ 
                Student(1, "Name2"),
                Student(2, "Name3"),
                Student(3, "foo"),
                Student(4, "Name1")
            ])
        l.SetQueryOptions("Name", 'name', False, 'Name', True)
        self.assertEqual(len(l.QueryIDs), 3)
        self.assertEqual(l[0, True].Name, "Name3")
        self.assertEqual(l[1, True].Name, "Name2")
        self.assertEqual(l[2, True].Name, "Name1")
        l.SetQueryOptions("Name", "name", True, 'ID', False)
        self.assertEqual(len(l.QueryIDs), 0)
        l.SetQueryOptions("Name", "foo", True, None, False)
        self.assertEqual(len(l.QueryIDs), 1)
        with self.assertRaises(InvalidParametersError):
            l["foo"]
if __name__ == '__main__':
    unittest.main()
