import unittest
from Service.Service import Service
from Domain.Student import Student
from Domain.Discipline import Discipline
from Domain.Grade import Grade
from Domain.CustomErrors import *

class Test_Service(unittest.TestCase):
    def test___init__(self):
        s = Service(True)
        self.assertEqual(s.StudentList.Length(), 10)
        self.assertEqual(s.DisciplineList.Length(), 10)
        self.assertEqual(s.GradeList.Length(), 10)

    def test_AddStudent(self):
        s = Service()
        s.AddStudent("Name")
        self.assertEqual(s.StudentList[s.StudentList.IDs[0]].Name, "Name")

    def test_AddDiscipline(self):
        s = Service()
        s.AddDiscipline("Name")
        self.assertEqual(s.DisciplineList[s.DisciplineList.IDs[0]].Name, "Name")
    
    def test_AddGrade(self):
        s = Service()
        s.AddStudent("Name")
        s.AddDiscipline("Name")
        s.AddGrade(s.StudentList[s.StudentList.IDs[0]], s.DisciplineList[s.DisciplineList.IDs[0]], 10)
        self.assertEqual(s.GradeList[s.GradeList.IDs[0]].Value, 10.0)

    def test_RemoveStudent(self):
        s = Service()
        s.AddStudent("Name")
        s.RemoveStudent(s.StudentList[s.StudentList.IDs[0]])
        self.assertEqual(s.StudentList.Length(), 0)

    def test_RemoveDiscipline(self):
        s = Service()
        s.AddDiscipline("Name")
        s.RemoveDiscipline(s.DisciplineList[s.DisciplineList.IDs[0]])
        self.assertEqual(s.DisciplineList.Length(), 0)

    def test_RemoveGrade(self):
        s = Service()
        s.AddStudent("Name")
        s.AddDiscipline("Name")
        s.AddGrade(s.StudentList[s.StudentList.IDs[0]], s.DisciplineList[s.DisciplineList.IDs[0]], 10)
        s.RemoveGrade(s.GradeList[s.GradeList.IDs[0]])
        self.assertEqual(s.GradeList.Length(), 0)

    def test_UpdateStudent(self):
        s = Service()
        s.AddStudent("Name")
        s.UpdateStudent(s.StudentList[s.StudentList.IDs[0]], Student(1, "NewName"))
        self.assertEqual(s.StudentList[s.StudentList.IDs[0]].Name, "NewName")
        with self.assertRaises(NonExistentItemIDError):
            s.UpdateStudent(Student(2, "gg"), Student(2, "gg"))

    def test_UpdateDiscipline(self):
        s = Service()
        s.AddDiscipline("Name")
        s.UpdateDiscipline(s.DisciplineList[s.DisciplineList.IDs[0]], Discipline(1, "NewName"))
        self.assertEqual(s.DisciplineList[s.DisciplineList.IDs[0]].Name, "NewName")
        with self.assertRaises(NonExistentItemIDError):
            s.UpdateDiscipline(Discipline(2, "gg"), Discipline(2, "gg"))

    def test_GetFailingStudents(self):
        s = Service()
        self.assertEqual(len(s.GetFailingStudents()), 0)
        s = Service(True)
        s.GetFailingStudents()

    def test_GetBestSchoolSituation(self):
        s = Service()
        self.assertEqual(len(s.GetBestSchoolSituation()), 0)
        s = Service(True)
        s.GetBestSchoolSituation()

    def test_GetEasiestDisciplines(self):
        s = Service()
        self.assertEqual(len(s.GetEasiestDisciplines()), 0)
        s = Service(True)
        s.GetEasiestDisciplines()

    def test_Undo_Redo(self):
        s = Service(True)
        with self.assertRaises(NoMoreStepsError):
            s.Undo()
        with self.assertRaises(NoMoreStepsError):
            s.Redo()
        s.RemoveStudent(Student(1, "NameDoesNotMatter"))
        s.Undo()
        s.Redo()
if __name__ == '__main__':
    unittest.main()
