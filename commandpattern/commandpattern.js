// ===== ICommand Interface (Simulated with Base Class) =====
class ICommand {
  execute() {
    throw new Error('execute() must be implemented');
  }

  undo() {
    throw new Error('undo() must be implemented');
  }
}

// ===== Receiver: AirConditioner =====
class AirConditioner {
  constructor() {
    this.isOn = false;
    this.temperature = 0;
  }

  turnOnAC() {
    this.isOn = true;
    console.log('AC is ON');
  }

  turnOffAC() {
    this.isOn = false;
    console.log('AC is OFF');
  }

  setTemperature(temp) {
    this.temperature = temp;
    console.log('Temperature changed to:', this.temperature);
  }
}

// ===== Concrete Commands =====
class TurnACOnCommand extends ICommand {
  constructor(ac) {
    super();
    this.ac = ac;
  }

  execute() {
    this.ac.turnOnAC();
  }

  undo() {
    this.ac.turnOffAC();
  }
}

class TurnACOffCommand extends ICommand {
  constructor(ac) {
    super();
    this.ac = ac;
  }

  execute() {
    this.ac.turnOffAC();
  }

  undo() {
    this.ac.turnOnAC();
  }
}

// ===== Invoker: Remote Control =====
class MyRemoteControl {
  constructor() {
    this.command = null;
    this.acCommandHistory = [];
  }

  setCommand(command) {
    this.command = command;
  }

  pressButton() {
    if (this.command) {
      this.command.execute();
      this.acCommandHistory.push(this.command);
    }
  }

  undo() {
    if (this.acCommandHistory.length > 0) {
      const lastCommand = this.acCommandHistory.pop();
      lastCommand.undo();
    }
  }
}

// ===== Client Code =====
const ac = new AirConditioner();
const remote = new MyRemoteControl();

remote.setCommand(new TurnACOnCommand(ac));
remote.pressButton();  // AC is ON

remote.undo();         // AC is OFF
