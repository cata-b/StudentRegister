from Domain.BaseIDList import BaseIDList
from Domain.IDListAction import IDListAction
from Domain.Student import Student
from Domain.Discipline import Discipline
from Domain.Grade import Grade
import pyodbc

class StudentListDB(BaseIDList):
    def __init__(self, connection_string):
        super().__init__()
        try:
            self._connection = pyodbc.connect(connection_string, autocommit=True)
        except:
            raise ConnectionError("Could not connect to database.")
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM Students")
        for item in cursor.fetchall():
            self._content[item.ID] = Student(item.ID, item.Name)
            if item.ID > self._latest_ID:
                self._latest_ID = item.ID
        
    def AddItems(self, items):
        super().AddItems(items)
        cursor = self._connection.cursor()
        for item in items:
            cursor.execute(
                """
                SET IDENTITY_INSERT Students ON
                INSERT INTO Students (ID, Name) VALUES (?, ?)
                SET IDENTITY_INSERT Students OFF
                """, item.ID, item.Name)
    
    def RemoveItems(self, itemIDs):
        super().RemoveItems(itemIDs)
        cursor = self._connection.cursor()
        for itemID in itemIDs:
            cursor.execute(
                """
                DELETE FROM Grades WHERE StudentID = ?
                DELETE FROM Students WHERE ID = ?
                """, itemID, itemID)

    def UpdateItem(self, itemID, new_value):
        super().UpdateItem(itemID, new_value)
        if self.HasKey(itemID):
            cursor = self._connection.cursor()
            cursor.execute("UPDATE Students SET Name = ? WHERE ID = ?", new_value.Name, itemID)

    def _reverse_action(self, action, destlist):
        super()._reverse_action(action, destlist)
        cursor = self._connection.cursor()
        if action.Type == IDListAction.AddAction:
            for item in action.Items:
                cursor.execute(
                """
                DELETE FROM Grades WHERE StudentID = ?
                DELETE FROM Students WHERE ID = ?
                """, item.ID, item.ID)
        elif action.Type == IDListAction.RemoveAction:
            for item in action.Items:
                cursor.execute(
                """
                SET IDENTITY_INSERT Students ON
                INSERT INTO Students (ID, Name) VALUES (?, ?)
                SET IDENTITY_INSERT Students OFF
                """, item.ID, item.Name)
        elif action.Type == IDListAction.UpdateAction:
            for item in action.Items:
                cursor.execute("UPDATE Students SET Name = ? WHERE ID = ?", item.Name, item.ID)

class DisciplineListDB(BaseIDList):
    def __init__(self, connection_string):
        super().__init__()
        try:
            self._connection = pyodbc.connect(connection_string, autocommit=True)
        except:
            raise ConnectionError("Could not connect to database.")
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM Disciplines")
        for item in cursor.fetchall():
            self._content[item.ID] = Discipline(item.ID, item.Name)
            if item.ID > self._latest_ID:
                self._latest_ID = item.ID
        
    def AddItems(self, items):
        super().AddItems(items)
        cursor = self._connection.cursor()
        for item in items:
            cursor.execute(
                """
                SET IDENTITY_INSERT Disciplines ON
                INSERT INTO Disciplines (ID, Name) VALUES (?, ?)
                SET IDENTITY_INSERT Disciplines OFF
                """, item.ID, item.Name)
    
    def RemoveItems(self, itemIDs):
        super().RemoveItems(itemIDs)
        cursor = self._connection.cursor()
        for itemID in itemIDs:
            cursor.execute(
                """
                DELETE FROM Grades WHERE DisciplineID = ?
                DELETE FROM Disciplines WHERE ID = ?
                """, itemID, itemID)

    def UpdateItem(self, itemID, new_value):
        super().UpdateItem(itemID, new_value)
        if self.HasKey(itemID):
            cursor = self._connection.cursor()
            cursor.execute("UPDATE Disciplines SET Name = ? WHERE ID = ?", new_value.Name, itemID)

    def _reverse_action(self, action, destlist):
        super()._reverse_action(action, destlist)
        cursor = self._connection.cursor()
        if action.Type == IDListAction.AddAction:
            for item in action.Items:
                cursor.execute(
                """
                DELETE FROM Grades WHERE DisciplineID = ?
                DELETE FROM Disciplines WHERE ID = ?
                """, item.ID, item.ID)
        elif action.Type == IDListAction.RemoveAction:
            for item in action.Items:
                cursor.execute(
                """
                SET IDENTITY_INSERT Disciplines ON
                INSERT INTO Disciplines (ID, Name) VALUES (?, ?)
                SET IDENTITY_INSERT Disciplines OFF
                """, item.ID, item.Name)
        elif action.Type == IDListAction.UpdateAction:
            for item in action.Items:
                cursor.execute("UPDATE Disciplines SET Name = ? WHERE ID = ?", item.Name, item.ID)

class GradeListDB(BaseIDList):
    def __init__(self, connection_string):
        super().__init__()
        try:
            self._connection = pyodbc.connect(connection_string, autocommit=True)
        except:
            raise ConnectionError("Could not connect to database.")
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM Grades")
        for item in cursor.fetchall():
            self._content[item.ID] = Grade(item.ID, item.StudentID, item.DisciplineID, item.Value)
            if item.ID > self._latest_ID:
                self._latest_ID = item.ID
        
    def AddItems(self, items):
        super().AddItems(items)
        cursor = self._connection.cursor()
        for item in items:
            cursor.execute(
                """
                SET IDENTITY_INSERT Grades ON
                INSERT INTO Grades (ID, StudentID, DisciplineID, Value) VALUES (?, ?, ?, ?)
                SET IDENTITY_INSERT Grades OFF
                """, item.ID, item.StudentID, item.DisciplineID, item.Value)
    
    def RemoveItems(self, itemIDs):
        super().RemoveItems(itemIDs)
        cursor = self._connection.cursor()
        for itemID in itemIDs:
            cursor.execute("DELETE FROM Grades WHERE ID = ?", itemID)

    def UpdateItem(self, itemID, new_value):
        super().UpdateItem(itemID, new_value)
        if self.HasKey(itemID):
            cursor = self._connection.cursor()
            cursor.execute("UPDATE Grades SET StudentID = ?, DisciplineID = ?, Value = ? WHERE ID = ?", new_value.StudentID, new_value.DisciplineID, new_value.Value, itemID)

    def _reverse_action(self, action, destlist):
        super()._reverse_action(action, destlist)
        cursor = self._connection.cursor()
        if action.Type == IDListAction.AddAction:
            for item in action.Items:
                cursor.execute("DELETE FROM Grades WHERE ID = ?", item.ID)
        elif action.Type == IDListAction.RemoveAction:
            for item in action.Items:
                cursor.execute(
                """
                SET IDENTITY_INSERT Grades ON
                INSERT INTO Grades (ID, StudentID, DisciplineID, Value) VALUES (?, ?, ?, ?)
                SET IDENTITY_INSERT Grades OFF
                """, item.ID, item.StudentID, item.DisciplineID, item.Value)
        elif action.Type == IDListAction.UpdateAction:
            for item in action.Items:
                cursor.execute("UPDATE Grades SET StudentID = ?, DisciplineID = ?, Value = ? WHERE ID = ?", item.StudentID, item.DisciplineID, item.Value, item.ID)