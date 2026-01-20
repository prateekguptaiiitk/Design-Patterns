from abc import ABC, abstractmethod

class DriveStrategy(ABC):
    @abstractmethod
    def drive(self):
        pass

class NormalDriveStrategy(DriveStrategy):
    def drive(self):
        print('Normal Drive Strategy')

class SportsDriveStrategy(DriveStrategy):
    def drive(self):
        print('Sports Drive Strategy')

class Vehicle:
    def __init__(self, strategy):
        self.strategy = strategy

    def drive(self):
        self.strategy.drive()

class OffRoadVehicle(Vehicle):
    def __init__(self):
        super().__init__(SportsDriveStrategy())

class PassengerVehicle(Vehicle):
    def __init__(self):
        super().__init__(NormalDriveStrategy())

# Testing the implementation
PassengerVehicle().drive()  # Output: Normal Drive Strategy
OffRoadVehicle().drive()    # Output: Sports Drive Strategy
