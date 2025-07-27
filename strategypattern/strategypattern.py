from __future__ import annotations
from abc import ABC, abstractmethod

class DriveStrategy(ABC):
    @abstractmethod
    def drive(self) -> None:
        pass

class NormalDriveStrategy(DriveStrategy):
    def drive(self) -> None:
        print('Normal Drive Strategy')

class SportsDriveStrategy(DriveStrategy):
    def drive(self) -> None:
        print('Sports Drive Strategy')

class Vehicle:
    def __init__(self, strategy: DriveStrategy) -> None:
        self.strategy = strategy

    def drive(self) -> None:
        self.strategy.drive()

class OffRoadVehicle(Vehicle):
    def __init__(self) -> None:
        super().__init__(SportsDriveStrategy())

class PassengerVehicle(Vehicle):
    def __init__(self) -> None:
        super().__init__(NormalDriveStrategy())

# Testing the implementation
PassengerVehicle().drive()  # Output: Normal Drive Strategy
OffRoadVehicle().drive()    # Output: Sports Drive Strategy
