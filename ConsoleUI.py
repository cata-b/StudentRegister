from Domain.Student import Student
from Domain.Discipline import Discipline
from Domain.Grade import Grade
from Domain.CustomErrors import *
import re


class ConsoleUI(object):
    """
    Class for showing a console menu to the user.
    """

    def __print_menu(self):
        print(\

"""0.Exit
Add:
    1. Student
    2. Discipline
    3. Grade
Show all:
    4. Students
    5. Disciplines
    6. Grades
Remove: (Will also remove all corresponding grades)
    7. Student 
    8. Discipline
Update:
    9. Student
    10. Discipline
Search:
    11. Student
    12. Discipline
Statistics:
    13. Failing students
    14. Students with the best school situation, sorted in descending order of their aggregated average
    15. All disciplines at  which there is at least one grade, sorted in descending order of the average 
        grade received by all students enrolled at that discipline.
16. Undo
17. Redo
""")

    def __add_student(self):
        sname = input("Enter student name: ")
        sname = sname.strip()
        if len(sname) == 0:
            print("Cannot add empty name.")
            return
        self.__service.AddStudent(sname)

    def __add_discipline(self):
        dname = input("Enter discipline name: ")
        dname = dname.strip()
        if len(dname) == 0:
            print("Cannot add empty name.")
            return
        self.__service.AddDiscipline(dname)

    def __select_student(self, slist):
        print("Select Student: ")
        self.__list_students()
        studentID = int(input("Student ID: "))
        if not slist.HasKey(studentID):
            raise Exception()
        return studentID

    def __select_discipline(self, dlist):
        print("Select discipline: ")
        self.__list_disciplines()
        disciplineID = int(input("Discipline ID: "))
        if not dlist.HasKey(disciplineID):
            raise Exception()
        return disciplineID

    def __list_students(self):
        print()
        student_list = self.__service.StudentList
        for ID in student_list.IDs:
            string = str(student_list[ID])
            print(string)
        print()

    def __list_disciplines(self):
        print()
        discipline_list = self.__service.DisciplineList
        for ID in discipline_list.IDs:
            print(str(discipline_list[ID]))
        print()

    def __list_grades(self):
        print()
        grade_list = self.__service.GradeList
        student_list = self.__service.StudentList
        discipline_list = self.__service.DisciplineList
        grade_list.SetQueryOptions(None, None, None, "ID", False)
        if grade_list.Length(True) == 0:
            print("No grades.")
            return
        print()
        for gradeID in grade_list.QueryIDs:
            print("Grade ID: %s\nStudent: %s\nDiscipline: %s\nValue: %s\n" % (gradeID, student_list[grade_list[gradeID].StudentID], discipline_list[grade_list[gradeID].DisciplineID], grade_list[gradeID].Value))


    def __add_grade(self):
        student_list = self.__service.StudentList
        discipline_list = self.__service.DisciplineList
        studentID = None
        disciplineID = None
        gradevalue = None
        try:
            studentID = self.__select_student(student_list)
            disciplineID = self.__select_discipline(discipline_list)
        except:
            print("Invalid ID.")
            print("Grade not added.")
            return

        try:
            gradevalue = float(input("Grade value: "))
        except:
            print("Invalid grade value.")
            print("Grade not added.")
            return

        try:
            self.__service.AddGrade(student_list[studentID], discipline_list[disciplineID], gradevalue)
        except Exception as e:
            print(e)
            print("Grade not added.")


    def __remove_student(self):
        studentID = None
        student_list = self.__service.StudentList
        if len(student_list.IDs) == 0:
            print("No students.")
            return
        try:
            studentID = self.__select_student(student_list)
        except:
            print("Invalid ID.")
            return
        self.__service.RemoveStudent(student_list[studentID])


    def __remove_discipline(self):
        disciplineID = None
        discipline_list = self.__service.DisciplineList
        if len(discipline_list.IDs) == 0:
            print("No disciplines.")
            return
        try:
            disciplineID = self.__select_discipline(discipline_list)
        except:
            print("Invalid ID.")
            return
        self.__service.RemoveDiscipline(discipline_list[disciplineID])

    def __update_student(self):
        studentID = None
        student_list = self.__service.StudentList
        if len(student_list.IDs) == 0:
            print("No students.")
            return
        try:
            studentID = self.__select_student(student_list)
        except:
            print("Invalid ID.")
            return
        sname = input("Enter new student name: ")
        sname = sname.strip()
        if len(sname) == 0:
            print("Cannot add empty name.")
            return
        self.__service.UpdateStudent(student_list[studentID], Student(studentID, sname))


    def __update_discipline(self):
        disciplineID = None
        discipline_list = self.__service.DisciplineList
        if len(discipline_list.IDs) == 0:
            print("No disciplines.")
            return
        try:
            disciplineID = self.__select_discipline(discipline_list)
        except:
            print("Invalid ID.")
            return
        dname = input("Enter new discipline name: ")
        dname = dname.strip()
        if len(dname) == 0:
            print("Cannot add empty name.")
            return
        self.__service.UpdateDiscipline(discipline_list[disciplineID], Discipline(disciplineID, dname))

    def __search_student(self):
        searchBy = None
        slist = self.__service.StudentList
        try:
            searchBy = int(input("Search by: \n1. ID\n2. Name\nYour choice: "))
            if searchBy not in [1, 2]:
                raise Exception()
        except:
            print("Invalid choice.")
            return
        if searchBy == 1:
            slist.SetQueryOptions('ID', input("Enter the ID to look for: "), False, 'ID', False)
        else:
            slist.SetQueryOptions('Name', input("Enter the name to look for: "), False, 'ID', False)
        if slist.Length(True) == 0:
            print("No items match your search.")
        else:
            print("\nSearch result: \n")
            for ID in range(slist.Length(True)):
                print(slist[ID, True])

    def __search_discipline(self):
        searchBy = None
        dlist = self.__service.DisciplineList
        try:
            searchBy = int(input("Search by: \n1. ID\n2. Name\nYour choice: "))
            if searchBy not in [1, 2]:
                raise Exception()
        except:
            print("Invalid choice.")
            return
        if searchBy == 1:
            dlist.SetQueryOptions('ID', input("Enter the ID to look for: "), False, 'ID', False)
        else:
            dlist.SetQueryOptions('Name', input("Enter the name to look for: "), False, 'ID', False)
        if dlist.Length(True) == 0:
            print("No items match your search.")
        else:
            print("\nSearch result: \n")
            for ID in range(dlist.Length(True)):
                print(dlist[ID, True])

    def __failing_students(self):
        failing = self.__service.GetFailingStudents()
        if len(failing) == 0:
            print("No failing students.")
            return
        for fail_data in failing:
            print("%s failing at:" % str(fail_data[0]))
            for disciplines in fail_data[1]:
                print("    %s, Value: %s" % (str(disciplines[0]), str(disciplines[1])))
            print()

    def __best_students(self):
        best = self.__service.GetBestSchoolSituation()
        if len(best) == 0:
            print("Cannot compute aggregated average for any of the students; do they have grades?")
            return
        for tupl in best:
            print("Student %s, Average: %s" % (str(tupl[0]), str(tupl[1])))

    def __easiest_disciplines(self):
        dis = self.__service.GetEasiestDisciplines()
        if len(dis) == 0:
            print("Cannot compute average for any discipline; do they have grades?")
            return
        for tupl in dis:
            print("Discipline %s, Average: %s" % (str(tupl[0]), str(tupl[1])))

    def __undo(self):
        try:
            self.__service.Undo()
        except NoMoreStepsError as e:
            print(e)

    def __redo(self):
        try:
            self.__service.Redo()
        except NoMoreStepsError as e:
            print(e)

    def __init__(self, service):
        self.__service = service
        self.__actions = \
            {
                1: self.__add_student,
                2: self.__add_discipline,
                3: self.__add_grade,
                4: self.__list_students,
                5: self.__list_disciplines,
                6: self.__list_grades,
                7: self.__remove_student,
                8: self.__remove_discipline,
                9: self.__update_student,
                10: self.__update_discipline,
                11: self.__search_student,
                12: self.__search_discipline,
                13: self.__failing_students,
                14: self.__best_students,
                15: self.__easiest_disciplines,
                16: self.__undo,
                17: self.__redo,
            }

    def start(self):
        while True:
            cmd = None
            self.__print_menu()
            try:
                cmd = int(input("Your command: "))
            except:
                print("Invalid command.")
            if cmd == 0:
                break
            self.__actions[cmd]()
            print()

#################
if __name__ == "__main__":
    from Service.Service import Service
    from Domain.ProgramSettings import ProgramSettings
    UI = ConsoleUI(Service(ProgramSettings("settings.properties")))
    UI.start()
#################