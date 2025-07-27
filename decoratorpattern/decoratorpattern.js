// ===== Abstract BasePizza =====
class BasePizza {
  cost() {
    throw new Error('Abstract method "cost()" must be implemented');
  }
}

// ===== Concrete Pizza Classes =====
class Farmhouse extends BasePizza {
  cost() {
    return 200;
  }
}

class VegDelight extends BasePizza {
  cost() {
    return 120;
  }
}

class Margherita extends BasePizza {
  cost() {
    return 100;
  }
}

// ===== Topping Decorator =====
class ToppingDecorator extends BasePizza {
  constructor(basePizza) {
    super();
    this.basePizza = basePizza;
  }

  getBasePizzaCost() {
    return this.basePizza.cost();
  }

  cost() {
    throw new Error('Abstract method "cost()" must be implemented');
  }
}

// ===== Concrete Toppings =====
class ExtraCheese extends ToppingDecorator {
  constructor(basePizza) {
    super(basePizza);
  }

  cost() {
    return this.getBasePizzaCost() + 10;
  }
}

class Mushrooms extends ToppingDecorator {
  constructor(basePizza) {
    super(basePizza);
  }

  cost() {
    return this.getBasePizzaCost() + 15;
  }
}

// ===== Client Code =====
const pizza1 = new ExtraCheese(new Margherita());
console.log(pizza1.cost()); // 100 + 10 = 110

const pizza2 = new Mushrooms(new ExtraCheese(new Margherita()));
console.log(pizza2.cost()); // 100 + 10 + 15 = 125
