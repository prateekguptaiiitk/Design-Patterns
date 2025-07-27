// ===== Abstract StudentBuilder =====
class StudentBuilder {
  constructor() {
    this.rollNumber = 0;
    this.age = 0;
    this.name = null;
    this.fatherName = null;
    this.motherName = null;
    this.subjects = null;

    if (this.constructor === StudentBuilder) {
      throw new Error('Cannot instantiate abstract class StudentBuilder');
    }
  }

  setRollNumber(rollNumber) {
    this.rollNumber = rollNumber;
    return this;
  }

  setAge(age) {
    this.age = age;
    return this;
  }

  setName(name) {
    this.name = name;
    return this;
  }

  setFatherName(fatherName) {
    this.fatherName = fatherName;
    return this;
  }

  setMotherName(motherName) {
    this.motherName = motherName;
    return this;
  }

  setSubjects() {
    throw new Error('Abstract method "setSubjects()" must be implemented');
  }

  build() {
    return new Student(this);
  }
}

// ===== Concrete Builder: MBAStudentBuilder =====
class MBAStudentBuilder extends StudentBuilder {
  setSubjects() {
    this.subjects = [
      "Micro Economics",
      "Business Studies",
      "Operations Management"
    ];
    return this;
  }
}

// ===== Concrete Builder: EngineeringStudentBuilder =====
class EngineeringStudentBuilder extends StudentBuilder {
  setSubjects() {
    this.subjects = [
      "DSA",
      "OS",
      "Computer Architecture"
    ];
    return this;
  }
}

// ===== Product: Student =====
class Student {
  constructor(builder) {
    this.rollNumber = builder.rollNumber;
    this.age = builder.age;
    this.name = builder.name;
    this.fatherName = builder.fatherName;
    this.motherName = builder.motherName;
    this.subjects = builder.subjects;
  }

  printObject() {
    console.log(
      `roll number: ${this.rollNumber}, age: ${this.age}, name: ${this.name}, father name: ${this.fatherName}, mother name: ${this.motherName}, subjects: ${this.subjects.join(', ')}`
    );
  }
}

// ===== Director =====
class Director {
  constructor(studentBuilder) {
    this.studentBuilder = studentBuilder;
  }

  createStudent() {
    if (this.studentBuilder instanceof EngineeringStudentBuilder) {
      return this.createEngineeringStudent();
    } else if (this.studentBuilder instanceof MBAStudentBuilder) {
      return this.createMBAStudent();
    }
    return null;
  }

  createEngineeringStudent() {
    return this.studentBuilder
      .setRollNumber(1)
      .setAge(22)
      .setName("sj")
      .setSubjects()
      .build();
  }

  createMBAStudent() {
    return this.studentBuilder
      .setRollNumber(2)
      .setAge(24)
      .setName("sj")
      .setFatherName("MyFatherName")
      .setMotherName("MyMotherName")
      .setSubjects()
      .build();
  }
}

// ===== Main =====
const director1 = new Director(new EngineeringStudentBuilder());
const director2 = new Director(new MBAStudentBuilder());

const engineeringStudent = director1.createStudent();
const mbaStudent = director2.createStudent();

engineeringStudent.printObject();
mbaStudent.printObject();
