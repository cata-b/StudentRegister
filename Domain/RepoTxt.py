from Domain.BaseIDList import BaseIDList
from Domain.Student import Student
from Domain.Discipline import Discipline
from Domain.Grade import Grade
from Domain.CustomErrors import *

class StudentListTxt(BaseIDList):

    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        try:
            r = open(self.__file, 'r')
        except OSError:
            raise FileNotFoundError("Couldn't load file: " + self.__file)
        line = r.readline().strip()
        items = []
        while line != "":
            try:
                data = line.split(",")
                items.append(Student(int(data[0]), data[1]))
            except:
                raise SyntaxError("File \"%s\" format is incorrect." % self.__file)
            line = r.readline().strip()
        try:
            self.AddItems(items)
            self._undo_list.clear()
        except InvalidParametersError:
            raise SyntaxError("File \"%s\" format is incorrect." % self.__file)
        except IDExistsError:
            raise SyntaxError("File \"%s\" contains duplicate ID.")
        r.close()

    def __save_items(self):
        w = open(self.__file, 'w')
        for sid in self.IDs:
            w.write("%s,%s\n" % (self[sid].ID, self[sid].Name))
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

class DisciplineListTxt(BaseIDList):

    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        try:
            r = open(self.__file, 'r')
        except OSError:
            raise FileNotFoundError("Couldn't load file: " + self.__file)
        line = r.readline().strip()
        items = []
        while line != "":
            try:
                data = line.split(",")
                items.append(Discipline(int(data[0]), data[1]))
            except:
                raise SyntaxError("File \"%s\" format is incorrect." % self.__file)
            line = r.readline().strip()
        try:
            self.AddItems(items)
            self._undo_list.clear()
        except InvalidParametersError:
            raise SyntaxError("File \"%s\" format is incorrect." % self.__file)
        except IDExistsError:
            raise SyntaxError("File \"%s\" contains duplicate ID.")
        r.close()

    def __save_items(self):
        w = open(self.__file, 'w')
        for did in self.IDs:
            w.write("%s,%s\n" % (self[did].ID, self[did].Name))
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

class GradeListTxt(BaseIDList):
    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        try:
            r = open(self.__file, 'r')
        except OSError:
            raise FileNotFoundError("Couldn't load file: " + self.__file)
        line = r.readline().strip()
        items = []
        while line != "":
            try:
                data = line.split(",")
                items.append(Grade(int(data[0]), int(data[1]), int(data[2]), float(data[3])))
            except:
                raise SyntaxError("File \"%s\" format is incorrect." % self.__file)
            line = r.readline().strip()
        try:
            self.AddItems(items)
            self._undo_list.clear()
        except InvalidParametersError:
            raise SyntaxError("File \"%s\" format is incorrect." % self.__file)
        except IDExistsError:
            raise SyntaxError("File \"%s\" contains duplicate ID.")
        r.close()

    def __save_items(self):
        w = open(self.__file, 'w')
        for gid in self.IDs:
            w.write("%s,%s,%s,%s\n" % (self[gid].ID, self[gid].StudentID, self[gid].DisciplineID, self[gid].Value))
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