// Abstract Implementor
class BreatheImplementor {
  breathe() {
    throw new Error('Method "breathe" must be implemented');
  }
}

// Concrete Implementors
class LandBreatheImplementation extends BreatheImplementor {
  breathe() {
    console.log('breathes through nose');
    console.log('inhale oxygen from air');
    console.log('exhale carbon dioxide');
  }
}

class WaterBreatheImplementation extends BreatheImplementor {
  breathe() {
    console.log('breathes through gills');
    console.log('inhale oxygen from water');
    console.log('exhale carbon dioxide');
  }
}

class TreeBreatheImplementation extends BreatheImplementor {
  breathe() {
    console.log('breathes through leaves');
    console.log('inhale carbon dioxide');
    console.log('exhale oxygen through photosynthesis');
  }
}

// Abstraction
class LivingThings {
  constructor(breatheImplementor) {
    if (new.target === LivingThings) {
      throw new Error("Cannot instantiate abstract class LivingThings directly");
    }
    this.breatheImplementor = breatheImplementor;
  }

  breatheProcess() {
    throw new Error('Method "breatheProcess" must be implemented');
  }
}

// Refined Abstractions
class Dog extends LivingThings {
  breatheProcess() {
    this.breatheImplementor.breathe();
  }
}

class Fish extends LivingThings {
  breatheProcess() {
    this.breatheImplementor.breathe();
  }
}

class Tree extends LivingThings {
  breatheProcess() {
    this.breatheImplementor.breathe();
  }
}

// Usage
const fish = new Fish(new WaterBreatheImplementation());
fish.breatheProcess();

console.log('---');

const tree = new Tree(new TreeBreatheImplementation());
tree.breatheProcess();
