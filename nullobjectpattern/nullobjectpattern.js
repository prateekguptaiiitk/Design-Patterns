// Abstract base class (simulated)
class Vehicle {
  getTankCapacity() {
    throw new Error("Method 'getTankCapacity()' must be implemented");
  }

  getSeatingCapacity() {
    throw new Error("Method 'getSeatingCapacity()' must be implemented");
  }
}

class VehicleFactory {
  static getVehicleObject(typeOfVehicle) {
    if (typeOfVehicle === "Car") {
      return new Car();
    }
    return new NullVehicle();
  }
}

class NullVehicle extends Vehicle {
  getTankCapacity() {
    return 0;
  }

  getSeatingCapacity() {
    return 0;
  }
}

class Car extends Vehicle {
  getTankCapacity() {
    return 40;
  }

  getSeatingCapacity() {
    return 5;
  }
}

// ---- Client code ----
const vehicle = VehicleFactory.getVehicleObject("Bike");
// const vehicle = VehicleFactory.getVehicleObject("Car");

console.log("Seating Capacity:", vehicle.getSeatingCapacity());
console.log("Fuel Tank Capacity:", vehicle.getTankCapacity());
