# Prototype Pattern

The **Prototype Design Pattern** allows new objects to be created by **cloning existing objects** rather than instantiating them directly. This is useful when object creation is costly or complex.

Below are the **key participants**, explained clearly and mapped directly to your `Student` example.

## 1. Prototype

### Responsibility

* Declares an interface for cloning itself.
* Ensures all concrete prototypes implement a `clone()` method.

### Code Snippet

```python
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass
```

---

## 2. Concrete Prototype

### Responsibility

* Implements the `clone()` method.
* Creates and returns a copy of itself (shallow or deep).

### Code Snippet

```python
class Student(Prototype):
    def __init__(self, age=None, roll_number=None, name=None):
        self.age = age
        self.roll_number = roll_number
        self.name = name
        
    def clone(self):
        return Student(self.age, self.roll_number, self.name)
```

---

## 3. Client

### Responsibility

* Uses the prototype’s `clone()` method to create new objects.
* Does not depend on concrete classes or constructors.

### Code Snippet

```python
obj = Student(20, 75, 'John')
clone_obj = obj.clone()
```

---

## Key Insight

> The Prototype Pattern transfers object creation responsibility from the client to the object itself.

---

## One-Line Interview Answer

> *Prototype Pattern consists of a Prototype interface, Concrete Prototype, and Client, enabling object creation by cloning existing instances.*

---

## Shallow vs Deep Copy (Quick Note)

* Above implementation performs a **shallow copy**, which is safe because it contains only primitive fields.
* For nested mutable objects, a **deep copy** should be used.
  ```python
    import copy
    
    def clone(self):
        return copy.deepcopy(self)
  ```
