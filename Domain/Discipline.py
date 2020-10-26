from Domain.BaseID import BaseID
from Domain.CustomErrors import InvalidParametersError

class Discipline(BaseID):
    """
    Class for representing disciplines.
    Properties: ID - int, Name - str
    """
    def __init__(self, ID, Name):
        if not isinstance(Name, str):
            raise InvalidParametersError("Name should be str.")
        self.__name = Name
        super().__init__(ID)
    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, value):
        if not isinstance(value, str):
            raise InvalidParametersError("Value should be str.")
        self.__name = value
    def __str__(self):
        return "ID: %s, Name: %s" % (self._BaseID__id, self.__name)

