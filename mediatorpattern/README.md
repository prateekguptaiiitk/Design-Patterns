# Mediator Design Pattern – Key Participants

The **Mediator Design Pattern** defines an object that encapsulates how a set of objects interact. It promotes **loose coupling** by preventing objects from referring to each other directly and instead lets them communicate through a mediator.

## 1. Mediator (Interface / Abstract Class)

### Responsibility

* Defines an interface for communication between colleague objects

### Key Points

* Centralizes interaction logic
* Colleagues communicate **only through the mediator**

### Typical Operations

```text
notify()
send()
coordinate()
```

### Example

```python
class Mediator:
    def notify(sender, event): pass
```

---

## 2. ConcreteMediator

### Responsibility

* Implements the Mediator interface
* Knows and manages all colleague objects
* Encapsulates how colleagues interact

### Key Points

* Controls workflow and communication rules
* Eliminates direct dependencies between colleagues

### Example

* Auction mediator
* Chat room
* Air traffic controller

```python
class Auction(Mediator):
    def place_bid(self, bidder, amount): ...

```

---

## 3. Colleague (Abstract Class / Interface)

### Responsibility

* Defines an interface for colleague objects
* Maintains a reference to the mediator

### Key Points

* Colleagues never communicate with each other directly
* All interaction is routed through the mediator

### Example

```python
class Colleague:
    def action(): pass
```

---

## 4. ConcreteColleague

### Responsibility

* Implements the Colleague interface
* Sends requests to the mediator
* Receives notifications from the mediator

### Key Points

* Contains only domain-specific logic
* Delegates coordination responsibility to the mediator

### Example

```python
class Bidder(Colleague):
    def place_bid(self, amount):
        mediator.place_bid(self, amount)
```

---

## 5. Client

### Responsibility

* Creates mediator and colleague objects
* Registers colleagues with the mediator

### Key Points

* Does not contain communication logic
* Only wires objects together

### Example

```python
auction = Auction()
bidder1 = Bidder("A", auction)
```

---

## Participant Collaboration Diagram

```
Client
  |
  v
ConcreteMediator
  /        \
Colleague  Colleague
```

All communication flows **through the mediator**.

---

## Summary Table

| Participant       | Responsibility                 |
| ----------------- | ------------------------------ |
| Mediator          | Defines communication contract |
| ConcreteMediator  | Coordinates interaction logic  |
| Colleague         | Declares operations            |
| ConcreteColleague | Executes actions via mediator  |
| Client            | Wires system together          |

---

## Interview One-Liner

> **Mediator pattern participants are:**
> **Mediator, ConcreteMediator, Colleague, ConcreteColleague, and Client.**

---

## Key Benefits

* Loose coupling
* Centralized interaction logic
* Improved maintainability

---

## Trade-Off (Important for Interviews)

> The mediator can become a **God Object** if it accumulates too much responsibility.

---

## Common Use Cases

* Chat applications
* GUI components interaction
* Workflow engines
* Auction systems

---

✅ **Mediator pattern is ideal when many objects communicate in complex ways and direct dependencies become hard to manage.**
