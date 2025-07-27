// ===== Strategy Interface (simulated with base class) =====
class DriveStrategy {
  drive() {
    throw new Error('Method "drive()" must be implemented');
  }
}

// ===== Concrete Strategies =====
class NormalDriveStrategy extends DriveStrategy {
  drive() {
    console.log("Normal Drive Strategy");
  }
}

class SportsDriveStrategy extends DriveStrategy {
  drive() {
    console.log("Sports Drive Strategy");
  }
}

// ===== Vehicle (Context) =====
class Vehicle {
  constructor(strategy) {
    this.strategy = strategy;
  }

  drive() {
    this.strategy.drive();
  }
}

// ===== Concrete Vehicles (Configured with Strategy) =====
class OffRoadVehicle extends Vehicle {
  constructor() {
    super(new SportsDriveStrategy());
  }
}

class PassengerVehicle extends Vehicle {
  constructor() {
    super(new NormalDriveStrategy());
  }
}

// ===== Test the implementation =====
new PassengerVehicle().drive();  // Output: Normal Drive Strategy
new OffRoadVehicle().drive();    // Output: Sports Drive Strategy
