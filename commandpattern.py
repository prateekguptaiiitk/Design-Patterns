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

class MyRemoteControl:
    command = None
    AC_command_history = []

    def set_command(self, command):
        self.command = command
    
    def press_button(self):
        self.command.execute()
        self.AC_command_history.append(self.command)
    
    def undo(self):
        if len(self.AC_command_history):
            last_command = self.AC_command_history.pop()
            last_command.undo()

class AirConditioner:
    is_on = False
    temperature = 0

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