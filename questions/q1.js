/*
* How would you design an object cache using Prototype Pattern?
* This cache checks if some obj is in cache, if it is, it clones that obj to 
* retain it in its original form in cache while changing only cloned obj
*/

class Shape {
    constructor(type) {
        this.type = type
    }

    clone() {
        throw new Error('implement abstract method clone()')
    }

    draw() {
        console.log(`Drawing a ${this.type}`);
    }
}

// 2. Specific shape classes
class Circle extends Shape {
  constructor() {
    super("Circle");
    this.radius = 10;
  }

  clone() {
    return new Circle()
  }
}

class Square extends Shape {
  constructor() {
    super("Square");
    this.side = 20;
  }

  clone() {
    return new Square()
  }
}

// 3. Cache Manager using Prototype Pattern
class ShapeCache {
  constructor() {
    this.shapeMap = new Map();
  }

  // Preload some prototype objects
  loadCache() {
    const circle = new Circle();
    const square = new Square();
    this.shapeMap.set("circle", circle);
    this.shapeMap.set("square", square);
  }

  // Clone a prototype from the cache
  getShape(shapeId) {
    const cachedShape = this.shapeMap.get(shapeId);
    return cachedShape ? cachedShape.clone() : null;
  }
}

// 4. Usage
const shapeCache = new ShapeCache();
shapeCache.loadCache();

const shape1 = shapeCache.getShape("circle");
shape1.draw(); // Drawing a Circle
shape1.radius = 50; // modifying doesn't affect the cache

const shape2 = shapeCache.getShape("circle");
shape2.draw(); // Drawing a Circle
console.log(shape2.radius); // still 10, unaffected

/*
Best clone logic for all types of scenarios
clone() {
  return Object.assign(Object.create(Object.getPrototypeOf(this)), this);
}
*/