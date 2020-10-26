import unittest
from Domain.CustomErrors import *

class Test_CustomErrors(unittest.TestCase):
    def test_IDExistsError(self):
        with self.assertRaises(IDExistsError):
            raise IDExistsError()
    def test_InvalidParametersError(self):
        with self.assertRaises(InvalidParametersError):
            raise InvalidParametersError()
    def test_NoMoreStepsError(self):
        with self.assertRaises(NoMoreStepsError):
            raise NoMoreStepsError()
    def test_NonExistentItemIDError(self):
        with self.assertRaises(NonExistentItemIDError):
            raise NonExistentItemIDError()
if __name__ == '__main__':
    unittest.main()
