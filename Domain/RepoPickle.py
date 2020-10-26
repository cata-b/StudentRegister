import pickle
from Domain.BaseIDList import BaseIDList
from Domain.Student import Student
from Domain.Discipline import Discipline
from Domain.Grade import Grade
from Domain.CustomErrors import *


class StudentListPickle(BaseIDList):

    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        try:
            r = open(self.__file, 'rb')
            data = pickle.load(r)
            items = []
            for item in data:
                items.append(Student(item[1].ID, item[1].Name))
            self.AddItems(items)
            self._undo_list.clear()
        except OSError:
            raise FileNotFoundError("Couldn't load file: " + self.__file)
        except EOFError:
            pass
        r.close()

    def __save_items(self):
        w = open(self.__file, 'wb')
        pickle.dump(list(self._content.items()), w)
        w.close()

    def AddItems(self, items):
        super().AddItems(items)
        self.__save_items()

    def RemoveItems(self, itemIDs):
        super().RemoveItems(itemIDs)
        self.__save_items()

    def UpdateItem(self, itemID, new_value):
        super().UpdateItem(itemID, new_value)
        self.__save_items()

    def Undo(self):
        super().Undo()
        self.__save_items()
        
    def Redo(self):
        super().Redo()
        self.__save_items()

class DisciplineListPickle(BaseIDList):

    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        try:
            r = open(self.__file, 'rb')
            data = pickle.load(r)
            items = []
            for item in data:
                items.append(Discipline(item[1].ID, item[1].Name))
            self.AddItems(items)
            self._undo_list.clear()
        except OSError:
            raise FileNotFoundError("Couldn't load file: " + self.__file)
        except EOFError:
            pass
        r.close()

    def __save_items(self):
        w = open(self.__file, 'wb')
        pickle.dump(list(self._content.items()), w)
        w.close()

    def AddItems(self, items):
        super().AddItems(items)
        self.__save_items()

    def RemoveItems(self, itemIDs):
        super().RemoveItems(itemIDs)
        self.__save_items()

    def UpdateItem(self, itemID, new_value):
        super().UpdateItem(itemID, new_value)
        self.__save_items()

    def Undo(self):
        super().Undo()
        self.__save_items()
        
    def Redo(self):
        super().Redo()
        self.__save_items()

class GradeListPickle(BaseIDList):
    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        try:
            r = open(self.__file, 'rb')
            data = pickle.load(r)
            items = []
            for item in data:
                items.append(Grade(item[1].ID, item[1].StudentID, item[1].DisciplineID, item[1].Value))
            self.AddItems(items)
            self._undo_list.clear()
        except OSError:
            raise FileNotFoundError("Couldn't load file: " + self.__file)
        except EOFError:
            pass
        r.close()

    def __save_items(self):
        w = open(self.__file, 'wb')
        pickle.dump(list(self._content.items()), w)
        w.close()

    def AddItems(self, items):
        super().AddItems(items)
        self.__save_items()

    def RemoveItems(self, itemIDs):
        super().RemoveItems(itemIDs)
        self.__save_items()

    def UpdateItem(self, itemID, new_value):
        super().UpdateItem(itemID, new_value)
        self.__save_items()

    def Undo(self):
        super().Undo()
        self.__save_items()
        
    def Redo(self):
        super().Redo()
        self.__save_items()
