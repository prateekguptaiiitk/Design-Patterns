class DBConnection1 {
  constructor() {
    if (DBConnection1._conObject) {
      throw new Error("Use DBConnection1.getInstance()");
    }
    // initialization code
  }

  static _instance = new DBConnection1(); // Eagerly initialized

  static getInstance() {
    return DBConnection1._instance;
  }
}

class DBConnection2 {
  constructor() {
    if (DBConnection2._instance) {
      throw new Error("Use DBConnection2.getInstance()");
    }
    // Initialize only once
    DBConnection2._instance = this;
  }

  static getInstance() {
    if (!DBConnection2._instance) {
      DBConnection2._instance = new DBConnection2();
    }
    return DBConnection2._instance;
  }
}

class DBConnection4 {
  constructor() {
    if (DBConnection4._conObject) {
      return DBConnection4._conObject;
    }
    DBConnection4._conObject = this;
    DBConnection4._lock = false
  }

  static getInstance() {
    if (!DBConnection4._conObject) {
      if (!DBConnection4._lock) {
        DBConnection4._lock = true;
        DBConnection4._conObject = new DBConnection4();
      }
    }
    return DBConnection4._conObject;
  }
}

// TEST: DBConnection1 class
const eager1 = DBConnection1.getInstance();
const eager2 = DBConnection1.getInstance();
console.log(`Eager Instance ID: ${eager1 === eager2}`); // true

// TEST: DBConnection2 class
const lazy1 = DBConnection2.getInstance();
const lazy2 = DBConnection2.getInstance();
console.log(`Lazy Instance ID: ${lazy1 === lazy2}`); // true
// new DBConnection(); // ❌ Throws error

// TEST: DBConnection4 class
const threadSafe1 = DBConnection4.getInstance();
const threadSafe2 = DBConnection4.getInstance();
console.log(`Thread-Safe Instance ID: ${threadSafe1 === threadSafe2}`); // true
