from abc import ABC, abstractmethod

class StudentBuilder(ABC):
    def __init__(self):
        self.roll_number = 0
        self.age = 0
        self.name = None
        self.father_name = None
        self.mother_name = None
        self.subjects = None

    def set_roll_number(self, roll_number):
        self.roll_number = roll_number
        return self
    
    def set_age(self, age):
        self.age = age
        return self
    
    def set_name(self, name):
        self.name = name
        return self
    
    def set_father_name(self, father_name):
        self.father_name = father_name
        return self
    
    def set_mother_name(self, mother_name):
        self.mother_name = mother_name
        return self
    
    @abstractmethod
    def set_subjects(self):
        pass
    
    def build(self):
        return Student(self)

class MBAStudentBuilder(StudentBuilder):
    def set_subjects(self):
        subs = []
        subs.append("Micro Economics")
        subs.append("Business Studies")
        subs.append("Operations Management")
        self.subjects = subs
        return self

class EngineeringStudentBuilder(StudentBuilder):
    def set_subjects(self):
        subs = []
        subs.append("DSA")
        subs.append("OS")
        subs.append("Computer Architecture")
        self.subjects = subs
        return self
    
class Student:
    def __init__(self, builder):
        self.roll_number = builder.roll_number
        self.age = builder.age
        self.name = builder.name
        self.father_name = builder.father_name
        self.mother_name = builder.mother_name
        self.subjects = builder.subjects

    def print_object(self):
        print("" , " roll number: ", self.roll_number, " age: ", self.age, " name: ", self.name, " father name: ", self.father_name, " mother name: ", self.mother_name, " subjects: ", self.subjects[0], ",", self.subjects[1], ",", self.subjects[2])

class Director:
    def __init__(self, student_builder):
        self.student_builder = student_builder
    
    def create_student(self):
        if isinstance(self.student_builder, EngineeringStudentBuilder):
            return self.create_engineering_student()
        elif isinstance(self.student_builder, MBAStudentBuilder):
            return self.create_mba_student()
        
        return None

    def create_engineering_student(self):
        return self.student_builder.set_roll_number(1).set_age(22).set_name("sj").set_subjects().build()
    
    def create_mba_student(self):
        return self.student_builder.set_roll_number(2).set_age(24).set_name("sj").set_father_name("MyFatherName").set_mother_name("MyMotherName").set_subjects().build()

if __name__ == '__main__':
    directorObj1 = Director(EngineeringStudentBuilder())
    directorObj2 = Director(MBAStudentBuilder())

    engineering_student = directorObj1.create_student()
    mba_student = directorObj2.create_student()

    engineering_student.print_object()
    mba_student.print_object()