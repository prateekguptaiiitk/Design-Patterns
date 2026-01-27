# Adapter Design Pattern – Key Participants

The **Adapter Pattern** allows incompatible interfaces to work together by converting one interface into another that the client expects.

## 🔑 Key Participants (GoF)

### 1️⃣ Target

* Defines the interface expected by the **client**
* Client interacts only with this interface

**In your code:**

```python
class WeighingMachineAdapter(ABC):
    @abstractmethod
    def getWeightInKg(self):
        pass
```

---

### 2️⃣ Adapter

* Implements the **Target** interface
* Wraps the **Adaptee**
* Converts requests from the Target format to the Adaptee format

**In your code:**

```python
class WeighingMachineAdapterImpl(WeighingMachineAdapter):
    def __init__(self, weighingMachine):
        self.weighingMachine = weighingMachine

    def getWeightInKg(self):
        weightInPound = self.weighingMachine.getWeightInPound()
        return weightInPound * 0.45
```

---

### 3️⃣ Adaptee

* Existing interface that is **incompatible** with the client
* Usually cannot be modified

**In your code:**

```python
class WeighingMachine(ABC):
    @abstractmethod
    def getWeightInPound(self):
        pass
```

---

### 4️⃣ Concrete Adaptee

* Actual implementation of the Adaptee
* Provides real functionality

**In your code:**

```python
class WeighingMachineForBabies(WeighingMachine):
    def __init__(self, weight):
        self.weight = weight

    def getWeightInPound(self):
        return self.weight
```

---

### 5️⃣ Client

* Uses only the **Target** interface
* Unaware of Adapter and Adaptee internals

**In your code:**

```python
weighingMachineAdapter = WeighingMachineAdapterImpl(WeighingMachineForBabies(50))
print(weighingMachineAdapter.getWeightInKg())
```

---

## 📊 Summary Table

| Participant      | Responsibility                      |
| ---------------- | ----------------------------------- |
| Target           | Interface expected by the client    |
| Adapter          | Converts Target requests to Adaptee |
| Adaptee          | Existing incompatible interface     |
| Concrete Adaptee | Actual implementation               |
| Client           | Uses Target interface               |

---

## 🎯 Interview-Friendly One-Liner

> **Adapter Pattern participants are:** Target, Adapter, Adaptee (and its concrete implementation), and Client.
