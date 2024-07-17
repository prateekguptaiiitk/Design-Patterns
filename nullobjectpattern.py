from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def getTankCapacity(self):
        pass

    @abstractmethod
    def getSeatingCapacity(self):
        pass

class VehicleFactory:

    @staticmethod
    def getVehicleObject(typeOfVehicle):
        if typeOfVehicle == 'Car':
            return Car()
        return NullVehicle()

class NullVehicle(Vehicle):
    def getTankCapacity(self):
        return 0

    def getSeatingCapacity(self):
        return 0

class Car(Vehicle):
    def getTankCapacity(self):
        return 40

    def getSeatingCapacity(self):
        return 5

if __name__ == '__main__':
    vehicle = VehicleFactory.getVehicleObject('Bike')
    # vehicle = VehicleFactory.getVehicleObject('Car')
    print("Seating Capacity: ", vehicle.getSeatingCapacity())
    print("Fuel Tank Capacity: ", vehicle.getTankCapacity())
