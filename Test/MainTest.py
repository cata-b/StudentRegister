if __name__ == "__main__":
    import unittest
    import Test.BaseID
    import Test.BaseIDList
    import Test.CustomErrors
    import Test.Discipline
    import Test.Grade
    import Test.IDListAction
    import Test.service
    import Test.Student
    modules = \
    [
        Test.BaseID,
        Test.BaseIDList,
        Test.CustomErrors,
        Test.Discipline,
        Test.Grade,
        Test.IDListAction,
        Test.service,
        Test.Student
    ]

    suite = unittest.TestSuite()
    for t in modules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(t))
    unittest.TextTestRunner().run(suite)
