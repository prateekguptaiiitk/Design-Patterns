// Originator
class ConfigurationOriginator {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }

  setHeight(height) {
    this.height = height;
  }

  setWidth(width) {
    this.width = width;
  }

  createMemento() {
    return new ConfigurationMemento(this.height, this.width);
  }

  restoreMemento(memento) {
    this.height = memento.getHeight();
    this.width = memento.getWidth();
  }
}

// Memento
class ConfigurationMemento {
  constructor(height, width) {
    this._height = height;
    this._width = width;
  }

  getHeight() {
    return this._height;
  }

  getWidth() {
    return this._width;
  }
}

// Caretaker
class ConfigurationCareTaker {
  constructor() {
    this.history = [];
  }

  addMemento(memento) {
    this.history.push(memento);
  }

  undo() {
    if (this.history.length > 0) {
      return this.history.pop();
    }
    return null;
  }
}

// Client
class Client {
  static run() {
    const careTaker = new ConfigurationCareTaker();
    const originator = new ConfigurationOriginator(5, 10);

    // Save snapshot 1
    const snapshot1 = originator.createMemento();
    careTaker.addMemento(snapshot1);

    // Modify and save snapshot 2
    originator.setHeight(7);
    originator.setWidth(12);
    const snapshot2 = originator.createMemento();
    careTaker.addMemento(snapshot2);

    // Modify again
    originator.setHeight(9);
    originator.setWidth(14);

    // Undo 1
    let restored = careTaker.undo();
    originator.restoreMemento(restored);
    console.log('height:', originator.height, 'width:', originator.width);

    // Undo 2
    restored = careTaker.undo();
    originator.restoreMemento(restored);
    console.log('height:', originator.height, 'width:', originator.width);
  }
}

// Run client
Client.run();
