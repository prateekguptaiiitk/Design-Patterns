# Command Design Pattern

The **Command Pattern** turns a request into an object.

Instead of calling a method directly on an object, the request is **encapsulated inside a command object**. This allows you to:

* Parameterize objects with different requests
* Queue or log operations
* Support **undo / redo** functionality
* Decouple the **invoker** from the **receiver**

> **Key idea:** The invoker does not know *how* the work is done—only *which command* to execute.

---

## Mapping the Pattern to the Code

### 1. Command (Interface / Abstract Class)

```python
class ICommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass
```

**Role:**

* Declares a common interface for all commands
* Enforces implementation of `execute()` and `undo()`

**Why it matters:**

* Enables polymorphism
* Allows the invoker to treat all commands uniformly

---

### 2. Concrete Commands

Examples:

* `TurnACOnCommand`
* `TurnACOffCommand`
* `SetTemperatureCommand`

```python
def execute(self):
    self.ac.turn_on_AC()
```

```python
def undo(self):
    self.ac.turn_off_AC()
```

**Responsibilities:**

* Implements the command interface
* Binds a receiver (`AirConditioner`)
* Stores state if required for undo

**Undo Support Example:**

```python
def execute(self):
    self.prev_temperature = self.ac.temperature
    self.ac.set_temperature(self.temperature)
```

This stored state enables proper undo behavior.

---

### 3. Receiver

```python
class AirConditioner:
```

**Role:**

* Contains the actual business logic
* Performs the requested operations

**Operations:**

* `turn_on_AC()`
* `turn_off_AC()`
* `set_temperature()`

> The receiver is completely unaware of command objects.

---

### 4. Invoker

```python
class MyRemoteControl:
```

**Role:**

* Triggers command execution
* Maintains command history for undo
* Does not know how the action is performed

```python
def press_button(self):
    self.command.execute()
    self.ac_command_history.append(self.command)
```

```python
def undo(self):
    last_command = self.ac_command_history.pop()
    last_command.undo()
```

**Benefit:**

* Complete decoupling from the receiver
* Works with any command implementing `ICommand`

---

### 5. Client

```python
if __name__ == '__main__':
```

**Role:**

* Creates the receiver
* Creates concrete command objects
* Assigns commands to the invoker

```python
remote.set_command(TurnACOnCommand(air_conditioner))
remote.press_button()
```

> The client wires all components together.

---

## Key Participants Summary

| Participant         | Code Example                               | Responsibility                        |
| ------------------- | ------------------------------------------ | ------------------------------------- |
| **Command**         | `ICommand`                                 | Declares command interface            |
| **ConcreteCommand** | `TurnACOnCommand`, `SetTemperatureCommand` | Implements command and binds receiver |
| **Receiver**        | `AirConditioner`                           | Performs actual work                  |
| **Invoker**         | `MyRemoteControl`                          | Executes commands and manages history |
| **Client**          | `main` block                               | Creates and configures commands       |

---

## When to Use the Command Pattern

Use the Command Pattern when:

* Undo / redo functionality is required
* UI must be decoupled from business logic
* Operations need to be queued, logged, or scheduled
* Behavior must be selected at runtime
