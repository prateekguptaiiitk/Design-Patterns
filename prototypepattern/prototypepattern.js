// ===== Abstract Prototype (simulated) =====
class Prototype {
  clone() {
    throw new Error('Abstract method "clone()" must be implemented');
  }
}

// ===== Concrete Prototype: Student =====
class Student extends Prototype {
  constructor(age = null, rollNumber = null, name = null) {
    super();
    this.age = age;
    this.rollNumber = rollNumber;
    this.name = name;
  }

  clone() {
    return new Student(this.age, this.rollNumber, this.name);
  }
}

// ===== Usage =====
const obj = new Student(20, 75, 'John');
const cloneObj = obj.clone();

console.log(`Original: age=${obj.age}, roll_number=${obj.rollNumber}, name=${obj.name}`);
console.log(`Clone: age=${cloneObj.age}, roll_number=${cloneObj.rollNumber}, name=${cloneObj.name}`);
