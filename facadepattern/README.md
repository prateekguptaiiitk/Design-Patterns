# Facade Pattern

The **Facade Design Pattern** provides a **simplified interface** to a complex subsystem, making it easier for clients to use while reducing coupling.

Below are the **key participants**, explained clearly and mapped directly to your order-processing example.

## 1. Facade

### Responsibility

* Provides a unified, high-level interface to the subsystem.
* Delegates client requests to appropriate subsystem objects.
* Hides the complexity of the subsystem from the client.

### Code Snippet

```python
class OrderFacade:
    def __init__(self):
        self.productDAO = ProductDAO()
        self.invoice = Invoice()
        self.payment = Payment()
        self.notification = SendNotification()
    
    def create_order(self, productID):
        self.productDAO.get_product(productID)
        self.payment.make_payment()
        self.invoice.generate_invoice()
        self.notification.send_notification()
        print('Order created successfully!')
```

---

## 2. Subsystem Classes

### Responsibility

* Implement the actual business logic.
* Perform the real work of the system.
* Are unaware of the Facade.

### Code Snippets

```python
class ProductDAO:
    def get_product(self, productID):
        print('Product with ID = ', productID)

class Payment:
    def make_payment(self):
        return True

class Invoice:
    def generate_invoice(self):
        print('invoice generated')

class SendNotification:
    def send_notification(self):
        print('notification sent')
```

---

## 3. Client

### Responsibility

* Uses the Facade to interact with the subsystem.
* Depends only on the Facade, not on subsystem classes.

### Code Snippet

```python
order_facade = OrderFacade()
order_facade.create_order(121)
```

---

## Key Insight

> The Facade Pattern simplifies interaction with a complex system without adding new functionality.

---

## One-Line Interview Answer

> *Facade Pattern consists of a Facade, Subsystem classes, and a Client, providing a simplified interface to a complex subsystem.*

---

## Facade vs Mediator (Quick Comparison)

| Facade                        | Mediator                              |
| ----------------------------- | ------------------------------------- |
| Simplifies subsystem usage    | Manages communication between objects |
| One-directional abstraction   | Two-way interaction                   |
| Subsystems do not know Facade | Colleagues know Mediator              |
