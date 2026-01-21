# Memento Design Pattern – Key Participants

The **Memento Design Pattern** (from the *Gang of Four*) captures and externalizes an object’s internal state **without violating encapsulation**, so that the object can later be restored to this state.

This document describes all **key participants**, their responsibilities, and how they collaborate.

## 🔑 Key Participants

### 1. Originator

**Responsibility**

* Creates a memento containing a snapshot of its current internal state.
* Restores its state from a given memento.

**Key Point**

* **Only the Originator** knows what state should be saved and how to restore it.

**Example**

```python
class ConfigurationOriginator:
    def create_memento(self):
        pass

    def restore_memento(self, memento):
        pass
```

---

### 2. Memento

**Responsibility**

* Stores the internal state of the Originator.
* Protects this state from access by other objects.

**Key Point**

* The memento is **opaque** to the Caretaker.
* It may expose its state only to the Originator.

**Example**

```python
class ConfigurationMemento:
    def __init__(self, state):
        self.__state = state
```

---

### 3. Caretaker

**Responsibility**

* Keeps track of mementos (for example, in a history stack).
* Never inspects or modifies the contents of a memento.

**Key Point**

* The Caretaker manages **history**, not state.

**Example**

```python
class ConfigurationCaretaker:
    def save(self, memento):
        pass

    def get_last(self):
        pass
```

---

## 🧩 Participant Relationship Diagram

```
Caretaker ---- stores ----> Memento
                               ^
                               |
                          Originator
                    (creates & restores)
```

---

## 🧠 Why These Participants Matter

| Participant | Purpose                 |
| ----------- | ----------------------- |
| Originator  | Owns and restores state |
| Memento     | Snapshot of state       |
| Caretaker   | Manages history         |

---

## ⚠️ Interview Insight

> **The Caretaker must not depend on the internal structure of the Memento.**

This preserves encapsulation and allows the Originator’s internal representation to change without impacting other objects.

---

## 📌 One-Line Interview Answer

> **Memento pattern participants are:** Originator, Memento, and Caretaker.

---

## 🆚 Common Interview Confusions

### Memento vs Command

| Memento             | Command            |
| ------------------- | ------------------ |
| Stores state        | Stores action      |
| Snapshot-based undo | Action-based undo  |
| Simple restore      | Complex undo logic |

---

**Summary**: The Memento pattern cleanly separates state preservation from business logic, making it ideal for undo/rollback functionality while maintaining strong encapsulation.
