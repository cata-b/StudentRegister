from Domain.CustomErrors import InvalidParametersError

class BaseID(object):
    """
    Base class for all classes that contain an integer ID.
    Properties: ID - int
    """

    def __init__(self, ID):
        if not isinstance(ID, int):
            raise InvalidParametersError("Parameter should be int.")
        self.__id = ID

    @property
    def ID(self):
        return self.__id
    @ID.setter
    def ID(self, value):
        if not isinstance(value, int):
            raise InvalidParametersError("Value is not an int.")
        self.__id = value