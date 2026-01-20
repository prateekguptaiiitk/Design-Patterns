# Visitor Design Pattern – Key Participants

The **Visitor Design Pattern** (from the *Gang of Four*) allows you to define new operations on a set of objects **without changing their classes**. It is especially useful when the object structure is stable but new operations need to be added frequently.

This document explains all **key participants**, their responsibilities, and how they collaborate.

## 🔑 Key Participants

### 1. Visitor (Interface / Abstract Class)

**Responsibility**

* Declares a `visit` method for **each concrete element type**.
* Enables **double dispatch** by allowing behavior to vary based on both visitor type and element type.

**Key Point**

* One visit method per concrete element.

**Example**

```python
class RoomVisitor(ABC):
    @abstractmethod
    def visit_single_room(self, room):
        pass

    @abstractmethod
    def visit_double_room(self, room):
        pass

    @abstractmethod
    def visit_delux_room(self, room):
        pass
```

---

### 2. ConcreteVisitor

**Responsibility**

* Implements the operations declared in the `Visitor` interface.
* Each concrete visitor represents a **new operation** on the elements.

**Key Point**

* Adding a new visitor = adding a new operation.

**Example**

```python
class RoomPricingVisitor(RoomVisitor):
    def visit_single_room(self, room):
        room.price = 1000

    def visit_double_room(self, room):
        room.price = 2000

    def visit_delux_room(self, room):
        room.price = 3000
```

---

### 3. Element (Interface / Abstract Class)

**Responsibility**

* Declares an `accept(visitor)` method.
* Allows a visitor to access the element.

**Key Point**

* Element hierarchy is assumed to be **stable**.

**Example**

```python
class RoomElement(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass
```

---

### 4. ConcreteElement

**Responsibility**

* Implements the `accept()` method.
* Calls the **type-specific visit method** on the visitor.
* Passes itself (`self`) to the visitor.

**Key Point**

* This is where **double dispatch** actually happens.

**Example**

```python
class SingleRoom(RoomElement):
    def accept(self, visitor):
        visitor.visit_single_room(self)
```

---

### 5. Object Structure (Optional but Common)

**Responsibility**

* Holds a collection of elements.
* Provides a way to apply visitors to all elements.

**Key Point**

* Often used to simplify client code.

**Example**

```python
class Hotel:
    def __init__(self, rooms):
        self.rooms = rooms

    def apply_visitor(self, visitor):
        for room in self.rooms:
            room.accept(visitor)
```

---

### 6. Client

**Responsibility**

* Creates concrete visitors.
* Applies them to elements (directly or via object structure).

**Example**

```python
pricing = RoomPricingVisitor()
hotel.apply_visitor(pricing)
```

---

## 🧩 Participant Relationship Diagram

```
Client
  |
  v
ObjectStructure ----> Element <---- ConcreteElement
                          |
                          v
                       Visitor <---- ConcreteVisitor
```

---

## 🧠 Why These Participants Matter

| Participant     | Purpose                    |
| --------------- | -------------------------- |
| Visitor         | Defines operations         |
| ConcreteVisitor | Implements new behavior    |
| Element         | Accepts visitors           |
| ConcreteElement | Enables double dispatch    |
| ObjectStructure | Manages element collection |
| Client          | Triggers operations        |

---

## ⚠️ Interview Insight

> **Visitor pattern favors adding new operations over adding new element types.**

Because:

* New visitors are easy to add
* New elements require changes in all visitors

---

## 📌 One-Line Interview Answer

> **Visitor pattern participants are:** Visitor, ConcreteVisitor, Element, ConcreteElement, ObjectStructure (optional), and Client.

---

**Summary**: The Visitor pattern uses double dispatch to separate operations from object structures, making it ideal when behavior changes frequently but the object model remains stable.
