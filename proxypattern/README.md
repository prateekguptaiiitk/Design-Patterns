# Proxy Design Pattern – Key Participants

The **Proxy Pattern** is a structural design pattern that provides a **surrogate or placeholder** for another object in order to **control access** to it.

Below are the **key participants** as defined by the GoF, mapped directly to your Proxy-pattern implementation.

## 1. Subject

### Responsibility

* Declares the common interface for both **RealSubject** and **Proxy**
* Allows the proxy to be used transparently in place of the real object

### Code Snippet

```python
class EmployeeDAO(ABC):
    @abstractmethod
    def create(self, client, employeeObj):
        pass

    @abstractmethod
    def delete(self, client, employeeId):
        pass

    @abstractmethod
    def get(self, client, employeeId):
        pass
```

### Key Point

> Subject defines *what operations are available*.

---

## 2. RealSubject

### Responsibility

* Implements the Subject interface
* Contains the **actual business logic**
* Performs real operations without access-control concerns

### Code Snippet

```python
class EmployeeDAOImpl(EmployeeDAO):
    def create(self, client, employeeObj):
        print('created a new row in employee table')

    def delete(self, client, employeeId):
        print('deleted a row with employee id:', employeeId)

    def get(self, client, employeeId):
        print('fetching data from the DB')
        return EmployeeDO("Dummy", employeeId)
```

### Key Point

> RealSubject does the real work.

---

## 3. Proxy

### Responsibility

* Implements the same interface as RealSubject
* Controls access to the RealSubject
* Delegates requests only when allowed
* Can add security, logging, caching, or lazy loading

### Code Snippet

```python
class EmployeeDAOProxy(EmployeeDAO):
    def __init__(self):
        self.employeeDAOObj = EmployeeDAOImpl()

    def create(self, client, employeeObj):
        if client == 'ADMIN':
            self.employeeDAOObj.create(client, employeeObj)
            return
        raise Exception('Access Denied!')
```

### Key Point

> Proxy decides *whether* to forward the request to the real object.

---

## 4. Client

### Responsibility

* Uses the Subject interface
* Interacts with the Proxy instead of the RealSubject
* Is unaware whether it is dealing with a proxy or the real object

### Code Snippet

```python
employeeTableObj = EmployeeDAOProxy()
employeeTableObj.create('USER', EmployeeDO('John', '23'))
```

### Key Point

> Client is decoupled from the real implementation.

---

## Types of Proxy (Interview Bonus)

* **Protection Proxy** → Access control (**used in your code**)
* **Virtual Proxy** → Lazy initialization
* **Remote Proxy** → Network communication
* **Caching Proxy** → Result caching
* **Logging Proxy** → Request logging

---

## Participant Mapping Summary

| GoF Participant | Your Code            |
| --------------- | -------------------- |
| Subject         | `EmployeeDAO`        |
| RealSubject     | `EmployeeDAOImpl`    |
| Proxy           | `EmployeeDAOProxy`   |
| Client          | `ProxyDesignPattern` |
| Domain Object   | `EmployeeDO`         |

---

## Interview One-Liner

> Proxy pattern provides a surrogate or placeholder for another object to control access to it.
