# Iterator Design Pattern – Key Participants

The **Iterator Design Pattern** (from the *Gang of Four*) provides a way to access elements of a collection sequentially **without exposing its internal representation**.

Below are all the **key participants**, their responsibilities, and how they collaborate.


## 🔑 Key Participants

### 1. Iterator (Interface / Abstract Class)

**Responsibility**

* Defines the interface for traversing elements.
* Provides operations for moving through a collection.

**Typical operations**

* `next()`
* `hasNext()`
* `currentItem()` *(optional)*
* `first()` *(optional)*

**Example**

```python
class Iterator(ABC):
    def has_next(self):
        pass

    def next(self):
        pass
```

---

### 2. ConcreteIterator

**Responsibility**

* Implements the `Iterator` interface.
* Maintains the **current traversal state** (index / pointer).
* Knows how to traverse the underlying collection.

**Key characteristics**

* Holds reference to the collection
* Tracks current position

**Example**

```python
class BookIterator(Iterator):
    def __init__(self, books):
        self.books = books
        self.index = 0
```

---

### 3. Aggregate (Interface / Abstract Class)

**Responsibility**

* Defines an interface for creating an iterator.
* Decouples the client from concrete collection classes.

**Typical operation**

* `createIterator()`

**Example**

```python
class Aggregate(ABC):
    def create_iterator(self):
        pass
```

---

### 4. ConcreteAggregate

**Responsibility**

* Implements the `Aggregate` interface.
* Stores the actual collection.
* Returns an appropriate concrete iterator.

**Example**

```python
class Library(Aggregate):
    def create_iterator(self):
        return BookIterator(self.book_list)
```

---

### 5. Client

**Responsibility**

* Uses only the `Iterator` interface.
* Does **not** access the collection directly.
* Controls traversal logic.

**Example**

```python
iterator = lib.create_iterator()

while iterator.has_next():
    book = iterator.next()
```

---

## 🧩 Participant Relationships

```
Client
  |
  v
Iterator <----- ConcreteIterator
  ^
  |
Aggregate <----- ConcreteAggregate
```

---

## 🧠 Why These Participants Matter

| Participant       | Purpose                                   |
| ----------------- | ----------------------------------------- |
| Iterator          | Separates traversal logic from collection |
| ConcreteIterator  | Maintains traversal state                 |
| Aggregate         | Hides collection implementation           |
| ConcreteAggregate | Creates correct iterator                  |
| Client            | Traverses without knowing internals       |

---

## ⚠️ Interview Insight

> The Iterator pattern encapsulates **both traversal logic and traversal state**, enabling flexible iteration strategies without breaking encapsulation.

---

## 🔁 Variants (Optional)

* Reverse Iterator
* Bidirectional Iterator
* Filtered Iterator
* Internal vs External Iterator

---

**Summary**: The Iterator pattern promotes clean separation of concerns, improves encapsulation, and makes collections easier to evolve without impacting clients.
