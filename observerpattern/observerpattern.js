// ===== Abstract Observable (Interface Simulation) =====
class StockObservable {
  add(observer) {
    throw new Error('Method "add()" must be implemented');
  }

  remove(observer) {
    throw new Error('Method "remove()" must be implemented');
  }

  notifySubscriber() {
    throw new Error('Method "notifySubscriber()" must be implemented');
  }

  setStockCount(newStockAdded) {
    throw new Error('Method "setStockCount()" must be implemented');
  }

  getStockCount() {
    throw new Error('Method "getStockCount()" must be implemented');
  }
}

// ===== Concrete Observable =====
class IphoneObservable extends StockObservable {
  constructor() {
    super();
    this.stockCount = 0;
    this.observers = [];
  }

  add(observer) {
    this.observers.push(observer);
  }

  remove(observer) {
    this.observers = this.observers.filter(obs => obs !== observer);
  }

  notifySubscriber() {
    for (const observer of this.observers) {
      observer.update();
    }
  }

  setStockCount(newStockAdded) {
    if (this.stockCount === 0 && newStockAdded > 0) {
      this.notifySubscriber();
    }
    this.stockCount += newStockAdded;
  }

  getStockCount() {
    return this.stockCount;
  }
}

// ===== Abstract Observer =====
class NotificationAlertObserver {
  update() {
    throw new Error('Method "update()" must be implemented');
  }
}

// ===== Concrete Observer: Email =====
class EmailAlertObserver extends NotificationAlertObserver {
  constructor(emailId, observable) {
    super();
    this.emailId = emailId;
    this.observable = observable;
  }

  update() {
    this.sendMessage("Product is back in stock");
  }

  sendMessage(msg) {
    console.log(`Email sent to: ${this.emailId}`);
  }
}

// ===== Concrete Observer: Mobile =====
class MobileAlertObserver extends NotificationAlertObserver {
  constructor(mobileNo, observable) {
    super();
    this.mobileNo = mobileNo;
    this.observable = observable;
  }

  update() {
    this.sendMessage("Product is back in stock");
  }

  sendMessage(msg) {
    console.log(`Message sent to mobile no.: ${this.mobileNo}`);
  }
}

// ===== Client Code =====
const iphoneStockObservable = new IphoneObservable();

const observer1 = new EmailAlertObserver("abc@gmail.com", iphoneStockObservable);
const observer2 = new EmailAlertObserver("xyz@gmail.com", iphoneStockObservable);
const observer3 = new MobileAlertObserver("1122334455", iphoneStockObservable);

iphoneStockObservable.add(observer1);
iphoneStockObservable.add(observer2);
iphoneStockObservable.add(observer3);

iphoneStockObservable.setStockCount(10);     // Should notify all
iphoneStockObservable.setStockCount(-10);    // Now stock is 0

iphoneStockObservable.remove(observer2);      // Remove one observer

iphoneStockObservable.setStockCount(40);     // Notify remaining
console.log("Current stock count:", iphoneStockObservable.getStockCount());
