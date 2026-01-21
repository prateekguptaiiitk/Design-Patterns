# Observer Design Pattern – Key Participants

The **Observer Design Pattern** defines a **one-to-many dependency** between objects so that when one object (the *Subject*) changes state, all its dependents (*Observers*) are notified automatically.

## 1. Subject (Observable)

### Responsibility

* Maintains a collection of observers
* Provides operations to:

  * attach (add) observers
  * detach (remove) observers
  * notify observers of state changes

### Key Point

* The Subject knows *that* observers exist, but not *how* they react.

### Typical Operations

```python
addObserver()
removeObserver()
notifyObservers()
```

**Example**

```python
class StockObservable(ABC):
    def add(self, observer):
        pass

    def remove(self, observer):
        pass

    def notify(self):
        pass

```

---

## 2. ConcreteSubject

### Responsibility

* Implements the Subject interface
* Stores the actual state of interest
* Triggers notifications when the state changes

### Key Point

* Decides **when** observers should be notified

### Example

* Stock inventory
* Weather data
* Order status

**Example**

```python
class IphoneObservable(StockObservable):
    def set_stock_count(self, count):
        self.stock_count = count
        self.notify()

```

---

## 3. Observer (Interface / Abstract Class)

### Responsibility

* Declares the `update()` method used by the Subject to notify observers

### Key Point

* Enables loose coupling between Subject and observers

### Typical Method

```python
update()
```

**Example**

```python
class NotificationAlertObserver(ABC):
    def update(self):
        pass

```

---

## 4. ConcreteObserver

### Responsibility

* Implements the Observer interface
* Defines how it reacts to state changes
* May fetch updated state from the Subject (**pull model**)
* Or receive data directly from the Subject (**push model**)

### Examples

* Email notification observer
* SMS notification observer
* UI refresh component

**Example**

```python
class EmailAlertObserver(NotificationAlertObserver):
    def update(self):
        print("Email sent")

```

---

## 5. Client

### Responsibility

* Creates Subject and Observer objects
* Registers and unregisters observers
* Configures the relationships between them

**Example**

```python
iphone_stock.add(emailObserver)
iphone_stock.add(mobileObserver)
```

---

## Participant Collaboration

```
Client
  |
  v
ConcreteSubject ---- maintains ----> Observer
        |                               ^
        |                               |
        -------- notify() -------- ConcreteObserver
```

---

## Why These Participants Matter

| Participant      | Purpose                       |
| ---------------- | ----------------------------- |
| Subject          | Manages observer registration |
| ConcreteSubject  | Holds and changes state       |
| Observer         | Defines update contract       |
| ConcreteObserver | Reacts to changes             |
| Client           | Wires everything together     |

---

## Interview One-Liner

> **Observer pattern participants are:**
> **Subject, ConcreteSubject, Observer, ConcreteObserver, and Client.**

---

## Key Benefits

* Loose coupling
* Easy extensibility
* Supports event-driven design

---

## Common Use Cases

* Stock price alerts
* Event listeners (UI frameworks)
* Cache invalidation
* Messaging systems

---

## Observer vs Pub-Sub (Interview Insight)

| Observer            | Pub-Sub             |
| ------------------- | ------------------- |
| Direct references   | Message broker      |
| Usually synchronous | Often asynchronous  |
| In-process          | Distributed systems |

---

✅ **The Observer pattern is foundational for reactive and event-driven architectures.**
