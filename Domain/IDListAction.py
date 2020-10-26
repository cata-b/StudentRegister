
class IDListAction(object):
    """
    Class for representing an action done on a BaseIDList instance.
    Properties: Items - list, Type - int
    Static properties: AddAction - int, RemoveAction - int, UpdateAction - int
    """
    
    AddAction = 0
    RemoveAction = 1
    UpdateAction = 2

    def __init__(self, type, items):
        self.__items = items
        self.__type = type

    @property
    def Items(self):
        return self.__items
    @property
    def Type(self):
        return self.__type