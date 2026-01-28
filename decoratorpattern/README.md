# Decorator Pattern

The **Decorator Pattern** allows behavior to be added to individual objects dynamically without modifying their existing class. It follows the **Open–Closed Principle** by favoring composition over inheritance.

Below are the **key participants**, explained conceptually and mapped directly to your pizza example code.

## 1. Component

### Responsibility

* Defines the common interface for objects that can have responsibilities added dynamically.
* Both concrete components and decorators implement this interface.

### Code Snippet

```python
class BasePizza(ABC):
    @abstractmethod
    def cost(self):
        pass
```

---

## 2. Concrete Component

### Responsibility

* Represents the original object to which new behavior can be added.
* Implements the Component interface.

### Code Snippets

```python
class Margheretta(BasePizza):
    def cost(self):
        return 100

class VegDelight(BasePizza):
    def cost(self):
        return 120

class Farmhouse(BasePizza):
    def cost(self):
        return 200
```

---

## 3. Decorator (Abstract Decorator)

### Responsibility

* Implements the Component interface.
* Holds a reference to a Component object.
* Delegates operations to the wrapped component.

### Code Snippet

```python
class ToppingDecorator(BasePizza):
    def __init__(self, base_pizza):
        self.base_pizza = base_pizza

    def cost(self):
        pass
```

---

## 4. Concrete Decorator

### Responsibility

* Adds additional responsibilities or behavior to the component.
* Extends functionality before or after delegating to the wrapped object.

### Code Snippets

```python
class ExtraCheese(ToppingDecorator):
    def cost(self):
        return self.base_pizza.cost() + 10

class Mushrooms(ToppingDecorator):
    def cost(self):
        return self.base_pizza.cost() + 15
```

---

## How the Decorator Pattern Works (Flow)

```python
pizza = Mushrooms(ExtraCheese(Margheretta()))
print(pizza.cost())
```

Execution order:

1. `Margheretta.cost()`
2. `ExtraCheese.cost()`
3. `Mushrooms.cost()`

Each decorator adds its own behavior and delegates the call forward.

---

## Interview One-Liner

> *The Decorator Pattern consists of a Component, Concrete Component, Decorator, and Concrete Decorator, allowing behavior to be added dynamically by wrapping objects instead of modifying their classes.*

---

## Decorator vs Inheritance

| Decorator Pattern             | Inheritance              |
| ----------------------------- | ------------------------ |
| Runtime behavior change       | Compile-time behavior    |
| Avoids subclass explosion     | Leads to many subclasses |
| Follows Open–Closed Principle | Often violates OCP       |
