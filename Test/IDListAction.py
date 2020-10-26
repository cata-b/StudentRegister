import unittest
from Domain.IDListAction import IDListAction

class Test_IDListAction(unittest.TestCase):
    def test___init__(self):
        a = IDListAction(IDListAction.AddAction, [])
        self.assertEqual(a.Type, IDListAction.AddAction)
        self.assertEqual(len(a.Items), 0)
        a = IDListAction(IDListAction.RemoveAction, [])
        self.assertEqual(a.Type, IDListAction.RemoveAction)
        self.assertEqual(len(a.Items), 0)
        a = IDListAction(IDListAction.UpdateAction, [])
        self.assertEqual(a.Type, IDListAction.UpdateAction)
        self.assertEqual(len(a.Items), 0)

if __name__ == '__main__':
    unittest.main()
