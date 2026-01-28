# Composite Pattern

The **Composite Design Pattern** allows you to compose objects into **tree structures** and lets clients treat **individual objects (Leaf)** and **compositions of objects (Composite)** uniformly.

Below are the **key participants**, explained conceptually and mapped directly to your file–directory example.

## 1. Component

### Responsibility

* Declares the common interface for all objects in the composition.
* Enables uniform treatment of Leaf and Composite objects.

### Code Snippet

```python
class FileSystem(ABC):
    @abstractmethod
    def ls(self):
        pass
```

---

## 2. Leaf

### Responsibility

* Represents end objects in the composition.
* Has no children.
* Implements behavior defined by the Component.

### Code Snippet

```python
class File(FileSystem):
    def __init__(self, name):
        self.fileName = name

    def ls(self):
        print("file name ", self.fileName)
```

---

## 3. Composite

### Responsibility

* Represents objects that can have children.
* Stores child components.
* Implements operations by delegating work to its children recursively.

### Code Snippet

```python
class Directory(FileSystem):
    def __init__(self, name):
        self.directoryName = name
        self.fileSystemList = []

    def add(self, fileSystemObj):
        self.fileSystemList.append(fileSystemObj)

    def ls(self):
        print("Directory name ", self.directoryName)
        for fileSystemObj in self.fileSystemList:
            fileSystemObj.ls()
```

---

## 4. Client (Optional but Commonly Mentioned)

### Responsibility

* Interacts with objects through the Component interface.
* Does not distinguish between Leaf and Composite objects.

### Code Snippet

```python
movieDirectory.ls()
```

---

## Key Insight

> The core idea of the Composite Pattern is that a client can treat a single object and a collection of objects in the same way.

---

## One-Line Interview Answer

> *Composite Pattern consists of a Component, Leaf, and Composite, allowing clients to treat individual objects and compositions uniformly.*

---

## Visual Structure (Your Example)

```
Movie (Directory)
 ├── Border (File)
 └── ComedyMovie (Directory)
       └── Hulchul (File)
```
