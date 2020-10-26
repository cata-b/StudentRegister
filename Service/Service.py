from Domain.BaseIDList import BaseIDList
from Domain.RepoTxt import *
from Domain.RepoPickle import *
from Domain.RepoDB import *
from Domain.RepoJSON import *
from Domain.Student import Student
from Domain.Discipline import Discipline
from Domain.Grade import Grade
from Domain.CustomErrors import *
from copy import deepcopy
import random

class Service(object):
    """
    Class that contains methods that work with 3 BaseIDList instances: of Student, of Discipline and of Grade
    """

    def __init__(self, settings):
        self.__data = None
        if settings["repository"] == "inmemory":
            self.__data = \
            {
                "s": BaseIDList(),
                "d": BaseIDList(),
                "g": BaseIDList()
            }
        elif settings["repository"] == "txt":
            self.__data = \
            {
                "s": StudentListTxt(settings["students"]),
                "d": DisciplineListTxt(settings["disciplines"]),
                "g": GradeListTxt(settings["grades"])
            }
        elif settings["repository"] == "pickle":
            self.__data = \
            {
                "s": StudentListPickle(settings["students"]),
                "d": DisciplineListPickle(settings["disciplines"]),
                "g": GradeListPickle(settings["grades"])
            }
        elif settings["repository"] == "json":
            self.__data = \
            {
                "s": StudentListJSON(settings["students"]),
                "d": DisciplineListJSON(settings["disciplines"]),
                "g": GradeListJSON(settings["grades"])
            }
        elif settings["repository"] == "db":
            self.__data = \
            {
                "s": StudentListDB(settings["db_connection_string"]),
                "d": DisciplineListDB(settings["db_connection_string"]),
                "g": GradeListDB(settings["db_connection_string"])
            }

        if self.__data == None:
            raise InvalidParametersError("Invalid settings.")
        self.__undo_list = []
        self.__redo_list = []
        if settings["debuglists"] == "True":
            self.__make_debug_lists()

    @property
    def StudentList(self):
        return self.__data['s']#deepcopy(self.__data['s'])
    @property
    def DisciplineList(self):
        return self.__data['d']# deepcopy(self.__data['d'])
    @property
    def GradeList(self):
        return self.__data['g']#deepcopy(self.__data['g'])

    def AddStudent(self, student_name):
        """
        Adds a student to the students list.
        May raise exceptions from the Student ctor.
        """
        self.__data['s'].AddItems([Student(self.__data['s'].GetSafeKey(), student_name)])
        self.__undo_list.append(['s'])
        self.__redo_list.clear()

    def AddDiscipline(self, discipline_name):
        """
        Adds a discipline to the disciplines list.
        May raise exceptions from the Discipline ctor.
        """
        self.__data['d'].AddItems([Discipline(self.__data['d'].GetSafeKey(), discipline_name)])
        self.__undo_list.append(['d'])
        self.__redo_list.clear()

    def AddGrade(self, student, discipline, grade_value):
        """
        Adds a discipline to the disciplines list.
        May raise exceptions from the Grade ctor.
        """
        if not self.__data['s'].HasKey(student.ID):
            raise NonExistentItemIDError("Student does not exist.")
        if not self.__data['d'].HasKey(discipline.ID):
            raise NonExistentItemIDError("Discipline does not exist.")
        self.__data['g'].AddItems([Grade(self.__data['g'].GetSafeKey(), student.ID, discipline.ID, grade_value)])
        self.__undo_list.append(['g'])
        self.__redo_list.clear()

    def RemoveStudent(self, student):
        """
        Removes a student (and their grades).
        Exceptions: NonExistentItemIDError if student.ID does not exist in the list.
        """
        if not self.__data['s'].HasKey(student.ID):
            raise NonExistentItemIDError("Student ID does not exist.")
        self.__data['s'].RemoveItems([student.ID])
        self.__data['g'].SetQueryOptions(FilterAttribute="StudentID", FilterValue=student.ID, StrictFilter=True)
        self.__data['g'].RemoveItems(self.__data['g'].QueryIDs)
        self.__undo_list.append(['s', 'g'])
        self.__redo_list.clear()

    def RemoveDiscipline(self, discipline):
        """
        Removes a discipline (and grades for it).
        Exceptions: NonExistentItemIDError if discipline.ID does not exist in the list.
        """
        if not self.__data['d'].HasKey(discipline.ID):
            raise NonExistentItemIDError("Discipline does not exist.")
        self.__data['d'].RemoveItems([discipline.ID])
        self.__data['g'].SetQueryOptions(FilterAttribute="DisciplineID", FilterValue=discipline.ID, StrictFilter=True)
        self.__data['g'].RemoveItems(self.__data['g'].QueryIDs)
        self.__undo_list.append(['d', 'g'])
        self.__redo_list.clear()

    def RemoveGrade(self, grade):
        """
        Removes a grade from the grades list.
        Exceptions: NonExistentItemIDError if grade.ID does not exist in the list.
        """
        if not self.__data['g'].HasKey(grade.ID):
            raise NonExistentItemIDError("Grade does not exist.")
        self.__data['g'].RemoveItems([grade.ID])
        self.__undo_list.append(['g'])
        self.__redo_list.clear()

    def UpdateStudent(self, student, new_student):
        """
        Updates a student.
        Exceptions: NonExistentItemIDError if student.ID does not exist in the list.
        """
        if not self.__data['s'].HasKey(student.ID):
            raise NonExistentItemIDError("Student does not exist.")
        self.__data['s'].UpdateItem(student.ID, new_student)
        self.__undo_list.append(['s'])
        self.__redo_list.clear()

    def UpdateDiscipline(self, discipline, new_discipline):
        """
        Updates a discipline.
        Exceptions: NonExistentItemIDError if discipline.ID does not exist in the list.
        """
        if not self.__data['d'].HasKey(discipline.ID):
            raise NonExistentItemIDError("Discipline does not exist.")
        self.__data['d'].UpdateItem(discipline.ID, new_discipline)
        self.__undo_list.append(['d'])
        self.__redo_list.clear()

    def GetFailingStudents(self):
        """
        Returns failing students as a list of [student, disc]
        where disc is a list of tuples of type (discipline, float)
        """
        slist = self.StudentList
        dlist = self.DisciplineList
        glist = self.GradeList
        failing_students = []
        for studentID in slist.IDs:
            glist.SetQueryOptions(FilterAttribute="StudentID", FilterValue=studentID, StrictFilter=True, OrderAttribute="ID", Descending=False)
            disc_sums = {}
            disc_count = {}
            for gradeID in glist.QueryIDs:
                if glist[gradeID].DisciplineID not in disc_sums:
                    disc_sums[glist[gradeID].DisciplineID] = glist[gradeID].Value
                    disc_count[glist[gradeID].DisciplineID] = 1
                else:
                    disc_sums[glist[gradeID].DisciplineID] += glist[gradeID].Value
                    disc_count[glist[gradeID].DisciplineID] += 1
            if len(disc_sums) == 0:
                continue
            failing_disciplines = []
            for discID in disc_sums:
                disc_sums[discID] /= disc_count[discID]
                if disc_sums[discID] < 5:
                    failing_disciplines.append(discID)
            if len(failing_disciplines) == 0:
                continue
            result = [slist[studentID], []]
            for discID in failing_disciplines:
                result[1].append((dlist[discID], disc_sums[discID]))
            failing_students.append(result)
        return failing_students

    def GetBestSchoolSituation(self):
        """
        Returns a list of tuples (student, avg) sorted descending by avg
        avg is the aggregated average for a student; where this cannot be computed the student will be missing from the list
        """
        slist = self.StudentList
        dlist = self.DisciplineList
        glist = self.GradeList
        student_avg_list = []
        for studentID in slist.IDs:
            glist.SetQueryOptions(FilterAttribute="StudentID", FilterValue=studentID, StrictFilter=True, OrderAttribute="ID", Descending=False)
            disc_sums = {}
            disc_count = {}
            for gradeID in glist.QueryIDs:
                if glist[gradeID].DisciplineID not in disc_sums:
                    disc_sums[glist[gradeID].DisciplineID] = glist[gradeID].Value
                    disc_count[glist[gradeID].DisciplineID] = 1
                else:
                    disc_sums[glist[gradeID].DisciplineID] += glist[gradeID].Value
                    disc_count[glist[gradeID].DisciplineID] += 1
            if len(disc_sums) == 0:
                continue
            sum = 0
            count = 0
            for discID in disc_sums:
                disc_sums[discID] /= disc_count[discID]
                sum += disc_sums[discID]
                count += 1
            student_avg_list.append((slist[studentID], float("%.3f" % (sum / count))))
        def get_avg_val(tupl):
            return tupl[1]
        student_avg_list = sorted(student_avg_list, key=get_avg_val, reverse=True)
        return student_avg_list

    def GetEasiestDisciplines(self):
        """
        Returns a list of tuples (discipline, avg) sorted descending by avg
        where avg is the average grade at that discipline; if discipline has no grades, it will not be added to the list
        """
        dlist = self.DisciplineList
        glist = self.GradeList
        result = []
        for disID in dlist.IDs:
            glist.SetQueryOptions(FilterAttribute="DisciplineID", FilterValue=disID, StrictFilter=False, OrderAttribute="ID", Descending=False)
            if glist.Length(True) == 0:
                continue
            avg = 0
            for gID in glist.QueryIDs:
                avg += glist[gID].Value
            avg /= glist.Length(True)
            result.append((dlist[disID], float("%.3f" % avg)))
        def get_tupl_avg(t):
            return t[1]
        return sorted(result, key=get_tupl_avg, reverse=True)

    def Undo(self):
        if len(self.__undo_list) == 0:
           raise NoMoreStepsError("No more undos.")
        last_operation = self.__undo_list.pop()
        for listID in last_operation:
            self.__data[listID].Undo()
        self.__redo_list.append(last_operation)

    def Redo(self):
        if len(self.__redo_list) == 0:
           raise NoMoreStepsError("No more redos.")
        last_operation = self.__redo_list.pop()
        for listID in last_operation:
            self.__data[listID].Redo()
        self.__undo_list.append(last_operation)

    def __make_random_word(self):
        vocals = "aeiouy"
        consonants = "bcdfghjklmnpqrstvwxz"
        result = str(consonants[random.randint(0, len(consonants) - 1)].upper())
        for i in range(random.randint(3, 6)):
                if i % 2 == 0:
                    result += vocals[random.randint(0, len(vocals) - 1)]
                else:
                    result += consonants[random.randint(0, len(consonants) - 1)]
        return result

    def __make_debug_lists(self):
        for _ in range(10):
            self.AddStudent(self.__make_random_word())
        for _ in range(10):
            self.AddDiscipline(self.__make_random_word())
        slist = self.StudentList
        dlist = self.DisciplineList
        for _ in range(10):
            self.AddGrade(slist[slist.IDs[random.randrange(1, len(slist.IDs))]], dlist[dlist.IDs[random.randrange(1, len(dlist.IDs))]], float("%.2f" % random.uniform(1, 10)))
        self.__undo_list.clear()
        self.__redo_list.clear()