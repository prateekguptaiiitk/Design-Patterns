// ===== Adaptee =====
class WeightMachine {
  getWeightInPound() {
    throw new Error('Abstract method "getWeightInPound()" must be implemented');
  }
}

class WeightMachineForBabies extends WeightMachine {
  getWeightInPound() {
    const weight = 56; // example weight
    return parseInt(weight, 10);
  }
}

// ===== Adapter Interface =====
class WeightMachineAdapter {
  getWeightInKg() {
    throw new Error('Abstract method "getWeightInKg()" must be implemented');
  }
}

// ===== Adapter Implementation =====
class WeightMachineAdapterImpl extends WeightMachineAdapter {
  constructor(weightMachine) {
    super();
    this.weightMachine = weightMachine;
  }

  getWeightInKg() {
    const weightInPound = this.weightMachine.getWeightInPound();
    const weightInKg = weightInPound * 0.45;
    return weightInKg;
  }
}

// ===== Client Code =====
const weightMachineAdapter = new WeightMachineAdapterImpl(
  new WeightMachineForBabies()
);
console.log(`Weight in Kg: ${weightMachineAdapter.getWeightInKg()}`);
