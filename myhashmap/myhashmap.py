class MyHashMap:
    INITIAL_SIZE = 1 << 4   # 16
    MAXIMUM_CAPACITY = 1 << 30

    def __init__(self):
        self.hashTable = [None] * self.INITIAL_SIZE

    @classmethod
    def initializeWithCapacity(cls, capacity):
        tableSize = cls.tableSizeFor(capacity)
        instance = cls()
        instance.hashTable = [None] * tableSize
        return instance

    class Entry:
        def __init__(self, k, v):
            self.key = k
            self.value = v
            self.next = None

    @staticmethod
    def tableSizeFor(cap):
        n = cap - 1
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        if n < 0:
            return 1
        else:
            if n >= MyHashMap.MAXIMUM_CAPACITY:
                return MyHashMap.MAXIMUM_CAPACITY
            else:
                return n + 1

    def put(self, key, value):
        hashCode = key % len(self.hashTable)
        node = self.hashTable[hashCode]

        if node is None:
            newNode = self.Entry(key, value)
            self.hashTable[hashCode] = newNode
        else:
            previousNode = node
            while node:
                if node.key == key:
                    node.value = value
                    return
                previousNode = node
                node = node.next
            newNode = self.Entry(key, value)
            previousNode.next = newNode

    def get(self, key):
        hashCode = key % len(self.hashTable)
        node = self.hashTable[hashCode]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        return None

if __name__ == '__main__':
    map = MyHashMap.initializeWithCapacity(7)

    map.put(1, "hi")
    map.put(2, "my")
    map.put(3, "name")
    map.put(4, "is")
    map.put(5, "John")
    map.put(6, "how")
    map.put(7, "are")
    map.put(8, "you")
    map.put(9, "friends")
    map.put(10, "?")

    value = map.get(8)
    print(value)
