from abc import ABC, abstractmethod

class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class Student(Prototype):
    def __init__(self, age=None, roll_number=None, name=None):
        self.age = age
        self.roll_number = roll_number
        self.name = name

    @classmethod
    def create_student(cls, age, roll_number, name):
        return cls(age, roll_number, name)

    def clone(self):
        return Student(self.age, self.roll_number, self.name)

if __name__ == '__main__':
    obj = Student.create_student(20, 75, 'John')
    clone_obj = obj.clone()

    print(f'Original: age={obj.age}, roll_number={obj.roll_number}, name={obj.name}')
    print(f'Clone: age={clone_obj.age}, roll_number={clone_obj.roll_number}, name={clone_obj.name}')
