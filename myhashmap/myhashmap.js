class Entry {
  constructor(key, value) {
    this.key = key;
    this.value = value;
    this.next = null;
  }
}

class MyHashMap {
  static INITIAL_SIZE = 1 << 4; // 16
  static MAXIMUM_CAPACITY = 1 << 30;

  constructor() {
    this.hashTable = new Array(MyHashMap.INITIAL_SIZE).fill(null);
  }

  static initializeWithCapacity(capacity) {
    const tableSize = MyHashMap.tableSizeFor(capacity);
    const instance = new MyHashMap();
    instance.hashTable = new Array(tableSize).fill(null);
    return instance;
  }

  static tableSizeFor(cap) {
    let n = cap - 1;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;

    if (n < 0) return 1;
    else if (n >= MyHashMap.MAXIMUM_CAPACITY) return MyHashMap.MAXIMUM_CAPACITY;
    else return n + 1;
  }

  put(key, value) {
    const hashCode = key % this.hashTable.length;
    let node = this.hashTable[hashCode];

    if (node === null) {
      this.hashTable[hashCode] = new Entry(key, value);
    } else {
      let prev = node;
      while (node !== null) {
        if (node.key === key) {
          node.value = value;
          return;
        }
        prev = node;
        node = node.next;
      }
      prev.next = new Entry(key, value);
    }
  }

  get(key) {
    const hashCode = key % this.hashTable.length;
    let node = this.hashTable[hashCode];

    while (node !== null) {
      if (node.key === key) {
        return node.value;
      }
      node = node.next;
    }

    return null;
  }
}

// Usage
const map = MyHashMap.initializeWithCapacity(7);

map.put(1, 'hi');
map.put(2, 'my');
map.put(3, 'name');
map.put(4, 'is');
map.put(5, 'John');
map.put(6, 'how');
map.put(7, 'are');
map.put(8, 'you');
map.put(9, 'friends');
map.put(10, '?');

const value = map.get(8);
console.log(value); // Output: "you"
