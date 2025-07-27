// ===== Abstract Factory Producer =====
class AbstractFactoryProducer {
  getFactoryInstance(value) {
    if (value === 'Economic') {
      return new EconomicCarFactory();
    } else if (value === 'luxury' || value === 'Premium') {
      return new LuxuryCarFactory();
    }
    return null;
  }
}

// ===== Abstract Factory Interface (simulated) =====
class AbstractFactory {
  getInstance(price) {
    throw new Error('Abstract method "getInstance()" must be implemented');
  }
}

// ===== Economic Car Factory =====
class EconomicCarFactory extends AbstractFactory {
  getInstance(price) {
    if (price <= 300000) {
      return new EconomicCar1();
    } else {
      return new EconomicCar2();
    }
  }
}

// ===== Luxury Car Factory =====
class LuxuryCarFactory extends AbstractFactory {
  getInstance(price) {
    if (price >= 1000000 && price <= 2000000) {
      return new LuxuryCar1();
    } else if (price > 2000000) {
      return new LuxuryCar2();
    }
    return null;
  }
}

// ===== Abstract Car Class (simulated) =====
class Car {
  getTopSpeed() {
    throw new Error('Abstract method "getTopSpeed()" must be implemented');
  }
}

// ===== Economic Cars =====
class EconomicCar1 extends Car {
  getTopSpeed() {
    return 100;
  }
}

class EconomicCar2 extends Car {
  getTopSpeed() {
    return 150;
  }
}

// ===== Luxury Cars =====
class LuxuryCar1 extends Car {
  getTopSpeed() {
    return 200;
  }
}

class LuxuryCar2 extends Car {
  getTopSpeed() {
    return 250;
  }
}

// ===== Usage =====
const abstractFactoryProducer = new AbstractFactoryProducer();
const factory = abstractFactoryProducer.getFactoryInstance('Premium');

const car = factory.getInstance(5000000);
console.log(car.getTopSpeed()); // Output: 250
