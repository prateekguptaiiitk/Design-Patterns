# Strategy Design Pattern – Key Participants

The **Strategy Design Pattern** (from the *Gang of Four*) defines a family of algorithms, encapsulates each one, and makes them interchangeable so that the algorithm can vary independently from the clients that use it.

This document explains all **key participants**, their responsibilities, and how they collaborate.

## 🔑 Key Participants

### 1. Strategy (Interface / Abstract Class)

**Responsibility**

* Declares a common interface for all supported algorithms.
* Ensures that all concrete strategies are interchangeable.

**Key Point**

* The context depends on this interface, not on concrete implementations.

**Example**

```python
class DriveStrategy(ABC):
    @abstractmethod
    def drive(self):
        pass
```

---

### 2. ConcreteStrategy

**Responsibility**

* Implements the algorithm defined by the `Strategy` interface.
* Each concrete strategy provides a different behavior.

**Key Point**

* Algorithms can vary independently of the context.

**Example**

```python
class NormalDriveStrategy(DriveStrategy):
    def drive(self):
        print("Normal Drive Strategy")

class SportsDriveStrategy(DriveStrategy):
    def drive(self):
        print("Sports Drive Strategy")
```

---

### 3. Context

**Responsibility**

* Maintains a reference to a `Strategy` object.
* Delegates the execution of the algorithm to the strategy.
* May allow the strategy to be changed at runtime.

**Key Point**

* Context does not know which concrete algorithm is being used.

**Example**

```python
class Vehicle:
    def __init__(self, strategy: DriveStrategy):
        self.strategy = strategy

    def drive(self):
        self.strategy.drive()
```

---

### 4. Client

**Responsibility**

* Creates and selects the appropriate `ConcreteStrategy`.
* Supplies the strategy to the context.
* Can switch strategies dynamically if needed.

**Key Point**

* Client controls *which* algorithm is used.

**Example**

```python
vehicle = Vehicle(NormalDriveStrategy())
vehicle.drive()
```

---

## 🧩 Participant Relationship Diagram

```
Client
  |
  v
Context ---------> Strategy
                      ^
                      |
               ConcreteStrategy
```

---

## 🧠 Why These Participants Matter

| Participant      | Purpose                            |
| ---------------- | ---------------------------------- |
| Strategy         | Defines common algorithm interface |
| ConcreteStrategy | Implements specific algorithms     |
| Context          | Delegates behavior to strategy     |
| Client           | Chooses and supplies algorithm     |

---

## ⚠️ Interview Insight

> The Strategy pattern separates **what** is done from **how** it is done, enabling runtime behavior changes and eliminating large conditional statements.

---

## 🆚 Common Interview Confusions

### Strategy vs State

| Strategy                   | State                                 |
| -------------------------- | ------------------------------------- |
| Client selects behavior    | Object changes behavior internally    |
| Algorithms are independent | Behavior depends on state transitions |

---

## 📌 One-Line Interview Answer

> **Strategy pattern participants are:** Strategy, ConcreteStrategy, Context, and Client.

---

**Summary**: The Strategy pattern promotes composition over inheritance, improves flexibility, and makes systems easier to extend and maintain.
