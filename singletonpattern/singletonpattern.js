class DBConnection1 {
  static _conObject = {};

  static getInstance() {
    return DBConnection1._conObject;
  }
}

class DBConnection2 {
  static _conObject = null;

  constructor() {
    if (DBConnection2._conObject) {
      return DBConnection2._conObject;
    }
    // Initialize only once
    DBConnection2._conObject = this;
  }

  static getInstance() {
    if (!DBConnection2._conObject) {
      DBConnection2._conObject = new DBConnection2();
    }
    return DBConnection2._conObject;
  }
}

class DBConnection4 {
  static _conObject = null;
  static _lock = false;

  constructor() {
    if (DBConnection4._conObject) {
      return DBConnection4._conObject;
    }
    DBConnection4._conObject = this;
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

// TEST: DBConnection4 class
const threadSafe1 = DBConnection4.getInstance();
const threadSafe2 = DBConnection4.getInstance();
console.log(`Thread-Safe Instance ID: ${threadSafe1 === threadSafe2}`); // true
