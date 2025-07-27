// Abstract Shape class
class Shape {
  draw() {
    throw new Error('Abstract method "draw()" must be implemented');
  }
}

// Rectangle class
class Rectangle extends Shape {
  draw() {
    console.log('It is Rectangle');
  }
}

// Circle class
class Circle extends Shape {
  draw() {
    console.log('It is Circle');
  }
}

// Square class
class Square extends Shape {
  draw() {
    console.log('It is Square');
  }
}

// ShapeFactory class
class ShapeFactory {
  getShape(input) {
    switch (input.toUpperCase()) {
      case 'CIRCLE':
        return new Circle();
      case 'RECTANGLE':
        return new Rectangle();
      default:
        return new Square();
    }
  }
}

// Usage
const shapeFactoryObj = new ShapeFactory();

const shapeObj1 = shapeFactoryObj.getShape('CIRCLE');   // Circle object
const shapeObj2 = shapeFactoryObj.getShape('SQUARE');   // Square object

shapeObj1.draw();
shapeObj2.draw();
