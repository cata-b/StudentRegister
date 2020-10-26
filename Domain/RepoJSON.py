from Domain.BaseIDList import BaseIDList
from Domain.Student import Student
from Domain.Discipline import Discipline
from Domain.Grade import Grade
from Domain.CustomErrors import *
import json

class StudentListJSON(BaseIDList):
    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        r = open(self.__file, 'r')
        file_content = r.read()
        r.close()
        if file_content != "":
            try:
                data = json.loads(file_content)
                items = []
                for record in data:
                    items.append(Student(record["ID"], record["Name"]))
                self.AddItems(items)
                self._undo_list.clear()
            except:
                raise SyntaxError("JSON file has an incorrect format.")


    def __save_items(self):
        w = open(self.__file, 'w')
        items = []
        for item in self._content.items():
            items.append({"ID": item[1].ID, "Name": item[1].Name})
        w.write(json.dumps(items, indent = 4))
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

class DisciplineListJSON(BaseIDList):
    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        r = open(self.__file, 'r')
        file_content = r.read()
        r.close()
        if file_content != "":
            try:
                data = json.loads(file_content)
                items = []
                for record in data:
                    items.append(Discipline(record["ID"], record["Name"]))
                self.AddItems(items)
                self._undo_list.clear()
            except:
                raise SyntaxError("JSON file has an incorrect format.")

    def __save_items(self):
        w = open(self.__file, 'w')
        items = []
        for item in self._content.items():
            items.append({"ID": item[1].ID, "Name": item[1].Name})
        w.write(json.dumps(items, indent = 4))
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

class GradeListJSON(BaseIDList):
    def __init__(self, filename):
        super().__init__()
        self.__file = filename
        self.__load_items()

    def __load_items(self):
        r = open(self.__file, 'r')
        file_content = r.read()
        r.close()
        if file_content != "":
            try:
                data = json.loads(file_content)
                items = []
                for record in data:
                    items.append(Grade(record["ID"], record["SID"], record["DID"], record["Val"]))
                self.AddItems(items)
                self._undo_list.clear()
            except:
                raise SyntaxError("JSON file has an incorrect format.")

    def __save_items(self):
        w = open(self.__file, 'w')
        items = []
        for item in self._content.items():
            items.append({"ID": item[1].ID, "SID": item[1].StudentID, "DID": item[1].DisciplineID, "Val": item[1].Value})
        w.write(json.dumps(items, indent = 4))
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