# Flyweight Design Pattern – Key Participants

The **Flyweight Pattern** is a structural design pattern used to **minimize memory usage** by sharing as much data as possible between similar objects.

Below are the **key participants** as defined by the GoF, mapped directly to your implementation.

## 1. Flyweight (Interface / Abstract Class)

### Responsibility

* Declares an interface for flyweight objects
* Defines operations that accept **extrinsic state** from the client

### Code Snippet

```python
class ILetter(ABC):
    @abstractmethod
    def display(self, row, col):
        pass
```

### Key Point

> This interface ensures all flyweight objects can be used interchangeably.

---

## 2. ConcreteFlyweight

### Responsibility

* Implements the Flyweight interface
* Stores **intrinsic (shared) state**
* Uses **extrinsic state** supplied by the client

### Code Snippet

```python
class DocumentCharacter(ILetter):
    def __init__(self, character, font_type, size):
        self.character = character      # intrinsic
        self.font_type = font_type      # intrinsic
        self.size = size                # intrinsic

    def display(self, row, col):        # extrinsic
        print('Character:', self.character,
              'font:', self.font_type,
              'Size:', self.size,
              'At position:', row, col)
```

### Key Point

> ConcreteFlyweight objects are shared and must be immutable with respect to intrinsic state.

---

## 3. FlyweightFactory

### Responsibility

* Creates and manages flyweight objects
* Ensures that identical flyweights are **reused**
* Acts as a cache for flyweight instances

### Code Snippet

```python
class LetterFactory:
    character_cache = {}

    @classmethod
    def create_letter(cls, character_value):
        if character_value not in cls.character_cache:
            cls.character_cache[character_value] = \
                DocumentCharacter(character_value, 'Arial', 10)
        return cls.character_cache[character_value]
```

### Key Point

> The factory prevents unnecessary object creation, enabling memory optimization.

---

## 4. Client

### Responsibility

* Maintains **extrinsic state**
* Requests flyweight objects from the factory
* Passes extrinsic state during method calls

### Code Snippet

```python
obj1 = LetterFactory.create_letter('t')
obj1.display(0, 0)

obj2 = LetterFactory.create_letter('t')
obj2.display(0, 6)
```

### Key Point

> Clients control context-specific data while sharing flyweight objects.

---

## Intrinsic vs Extrinsic State

| State Type | Stored In | Example               |
| ---------- | --------- | --------------------- |
| Intrinsic  | Flyweight | character, font, size |
| Extrinsic  | Client    | row, column           |

---

## Participant Mapping Summary

| GoF Participant   | Your Code           |
| ----------------- | ------------------- |
| Flyweight         | `ILetter`           |
| ConcreteFlyweight | `DocumentCharacter` |
| FlyweightFactory  | `LetterFactory`     |
| Client            | Main program        |

---

## Interview One‑Liner

> Flyweight pattern participants include Flyweight, ConcreteFlyweight, FlyweightFactory, and Client. The factory ensures reuse, flyweights store intrinsic state, and clients provide extrinsic state.
