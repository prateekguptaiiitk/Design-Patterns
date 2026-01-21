# Chain of Responsibility Pattern – Key Participants

The **Chain of Responsibility (CoR) Design Pattern** allows a request to be passed along a chain of handlers. Each handler decides whether to process the request or forward it to the next handler in the chain. This decouples the **sender** of a request from its **receiver(s)**.

## 1. Handler (Abstract Handler)

### Responsibility

* Declares an interface for handling requests
* Maintains a reference to the next handler in the chain

### Key Point

* Provides default behavior to forward the request to the next handler

### Typical Structure

```python
handle(request)
setNext(handler)
```

**Example**

```python
class Handler:
    def handle(self, request):
        if self.next:
            self.next.handle(request)
```

---

## 2. ConcreteHandler

### Responsibility

* Implements the Handler interface
* Decides whether to:

  * handle the request, or
  * pass it to the next handler

### Key Point

* Each ConcreteHandler handles **one specific responsibility**

### Examples

* InfoLogProcessor
* DebugLogProcessor
* ErrorLogProcessor

**Example**

```python
class ErrorHandler(Handler):
    def handle(self, request):
        if request.type == ERROR:
            process()
        else:
            super().handle(request)
```

---

## 3. Client

### Responsibility

* Creates and configures the chain of handlers
* Sends the request to the first handler in the chain

### Key Point

* Client is unaware of which handler will ultimately process the request

```python
handler1.set_next(handler2)
handler1.handle(request)
```

---

## 4. Request (Optional Participant)

### Responsibility

* Encapsulates the data being processed by the chain

### Key Point

* Can be a full object, enum, or simple method parameters

### Examples

* HTTP request
* Log message + log level
* Event object

**Example**

```python
class LogRequest:
    level
    message
```

---

## Participant Collaboration

```
Client
  |
  v
Handler ---> Handler ---> Handler
   (ConcreteHandlers linked in a chain)
```

---

## Why These Participants Matter

| Participant     | Purpose                        |
| --------------- | ------------------------------ |
| Handler         | Defines handling interface     |
| ConcreteHandler | Handles or forwards request    |
| Client          | Builds and starts the chain    |
| Request         | Carries data through the chain |

---

## Interview One-Liner

> **Chain of Responsibility participants are:**
> **Handler, ConcreteHandler, Client, and Request (optional).**

---

## Key Characteristics

* Loose coupling between sender and receiver
* Dynamic chain configuration
* Eliminates large `if-else` or `switch` statements

---

## Common Use Cases

* Logging frameworks
* Middleware pipelines
* Authentication / authorization filters
* Event processing systems

---

## Comparison Insight (Interview)

### Chain of Responsibility vs Command

| Chain of Responsibility     | Command                 |
| --------------------------- | ----------------------- |
| Multiple potential handlers | Single receiver         |
| Request flows through chain | Request is encapsulated |
| Runtime handler selection   | Explicit invocation     |

---

✅ **Chain of Responsibility is ideal for building flexible processing pipelines where the exact handler is determined at runtime.**
