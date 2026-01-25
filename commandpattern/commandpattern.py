from abc import ABC, abstractmethod

class ICommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class TurnACOnCommand(ICommand):
    def __init__(self, ac):
        self.ac = ac
    
    def execute(self):
        self.ac.turn_on_AC()
    
    def undo(self):
        self.ac.turn_off_AC()
    
class TurnACOffCommand(ICommand):
    def __init__(self, ac):
        self.ac = ac
    
    def execute(self):
        self.ac.turn_off_AC()

    def undo(self):
        self.ac.turn_on_AC()

class SetTemperatureCommand(ICommand):
    def __init__(self, ac, temperature):
        self.ac = ac
        self.temperature = temperature

    def execute(self):
        self.prev_temperature = self.ac.temperature
        self.ac.set_temperature(self.temperature)

    def undo(self):
        self.ac.set_temperature(self.prev_temperature)

class MyRemoteControl:
    def __init__(self):
        self.command = None
        self.ac_command_history = []

    def set_command(self, command):
        self.command = command
    
    def press_button(self):
        self.command.execute()
        self.ac_command_history.append(self.command)
    
    def undo(self):
        if len(self.ac_command_history):
            last_command = self.ac_command_history.pop()
            last_command.undo()

class AirConditioner:
    def __init__(self):
        self.is_on = False
        self.temperature = 0

    def turn_on_AC(self):
        self.is_on = True
        print('AC is ON')
    
    def turn_off_AC(self):
        self.is_on = False
        print('AC is OFF')
    
    def set_temperature(self, temperature):
        self.temperature = temperature
        print('Temperature changed to:', self.temperature)

if __name__ == '__main__':
    # AC object
    air_conditioner = AirConditioner()

    # remote
    remote = MyRemoteControl()

    # create command and press button
    remote.set_command(TurnACOnCommand(air_conditioner))
    remote.press_button()

    # undo the last operation
    remote.undo()

    # create command and press button
    remote.set_command(SetTemperatureCommand(air_conditioner, 24))
    remote.press_button()
    remote.set_command(SetTemperatureCommand(air_conditioner, 26))
    remote.press_button()

    # undo the last operation
    remote.undo()
