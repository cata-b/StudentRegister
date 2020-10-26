
from Domain.BaseID import BaseID
from Domain.CustomErrors import InvalidParametersError

class Grade(BaseID):
    """
    Class for representing grades.
    Properties: ID - int, StudentID - int, DisciplineID - int, Value - float in [0, 10]
    """
    def __init__(self, ID, StudentID, DisciplineID, Value):
        if not (isinstance(ID, int) and isinstance(StudentID, int) and isinstance(DisciplineID, int)):
            raise InvalidParametersError("Invalid parameters.")
        try:
            Value = float(Value)
            if Value < 0 or Value > 10:
                raise Exception()
        except:
            raise InvalidParametersError("Value should be a positive float <= 10.")
        
        self.__sid = StudentID
        self.__did = DisciplineID
        self.__val = Value
        super().__init__(ID)

    def __str__(self):
        return "ID: %s, StudentID: %s, DisciplineID: %s, Value: %s" % (self._BaseID__id, self.__sid, self.__did, self.__val)

    @property
    def StudentID(self):
        return self.__sid
    @StudentID.setter
    def StudentID(self, value):
        if not isinstance(value, int):
            raise InvalidParametersError("Value should be int.")
        self.__sid = value

    @property
    def DisciplineID(self):
        return self.__did
    @DisciplineID.setter
    def DisciplineID(self, value):
        if not isinstance(value, int):
            raise InvalidParametersError("Value should be int.")
        self.__did = value

    @property
    def Value(self):
        return self.__val
    @Value.setter
    def Value(self, value):
        try:
            value = float(value)
            if value < 0 or value > 10:
                raise Exception()
        except:
            raise InvalidParametersError("Value should be a positive float <= 10.")
        self.__val = value