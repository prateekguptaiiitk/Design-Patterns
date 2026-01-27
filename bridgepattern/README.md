# Bridge Design Pattern – Key Participants

The **Bridge Pattern** is a structural design pattern that **decouples an abstraction from its implementation**, allowing both to evolve independently.

Below are the **key participants** as defined by the GoF, mapped directly to your Bridge-pattern implementation.

## 1. Abstraction

### Responsibility

* Defines the high-level interface
* Maintains a reference to an **Implementor**
* Delegates implementation-specific work

### Code Snippet

```python
class LivingThings(ABC):
    def __init__(self, breathe_implementor):
        self.breathe_implementor = breathe_implementor

    @abstractmethod
    def breathe_process(self):
        pass
```

### Key Point

> The abstraction focuses on *what* is done, not *how* it is done.

---

## 2. Refined Abstraction

### Responsibility

* Extends the Abstraction
* May add or customize behavior
* Still delegates implementation details to the Implementor

### Code Snippet

```python
class Dog(LivingThings):
    def breathe_process(self):
        self.breathe_implementor.breathe()

class Fish(LivingThings):
    def breathe_process(self):
        self.breathe_implementor.breathe()

class Tree(LivingThings):
    def breathe_process(self):
        self.breathe_implementor.breathe()
```

### Key Point

> Multiple abstractions can reuse the same implementation.

---

## 3. Implementor

### Responsibility

* Defines the interface for implementation classes
* Does not need to mirror the abstraction interface

### Code Snippet

```python
class BreatheImplementor(ABC):
    @abstractmethod
    def breathe(self):
        pass
```

### Key Point

> Implementors define *how* the work is performed.

---

## 4. Concrete Implementor

### Responsibility

* Implements the Implementor interface
* Contains platform- or behavior-specific logic

### Code Snippet

```python
class LandBreatheImplementation(BreatheImplementor):
    def breathe(self):
        print('breathes through nose')

class WaterBreatheImplementation(BreatheImplementor):
    def breathe(self):
        print('breathes through gills')

class TreeBreatheImplementation(BreatheImplementor):
    def breathe(self):
        print('breathes through leaves')
```

### Key Point

> Implementations can vary independently of abstractions.

---

## 5. Client

### Responsibility

* Creates and connects Abstraction with Implementor
* Uses the abstraction, not concrete implementors

### Code Snippet

```python
fish_obj = Fish(WaterBreatheImplementation())
tree_obj = Tree(TreeBreatheImplementation())
```

### Key Point

> The client decides which implementation to use at runtime.

---

## Participant Mapping Summary

| GoF Participant      | Your Code                                                                              |
| -------------------- | -------------------------------------------------------------------------------------- |
| Abstraction          | `LivingThings`                                                                         |
| Refined Abstraction  | `Dog`, `Fish`, `Tree`                                                                  |
| Implementor          | `BreatheImplementor`                                                                   |
| Concrete Implementor | `LandBreatheImplementation`, `WaterBreatheImplementation`, `TreeBreatheImplementation` |
| Client               | Main program                                                                           |

---

## Interview One-Liner

> Bridge pattern separates abstraction from implementation so that both can evolve independently.
