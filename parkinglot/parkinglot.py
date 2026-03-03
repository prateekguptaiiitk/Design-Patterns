import threading
from typing import Dict, Optional, List
from collections import defaultdict
from enum import Enum
from abc import ABC, abstractmethod
import uuid
import time

class VehicleSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


# abstract class
class Vehicle(ABC):
    def __init__(self, license_number: str, size: VehicleSize):
        self.license_number = license_number
        self.size = size

    def get_license_number(self) -> str:
        return self.license_number

    def get_size(self) -> VehicleSize:
        return self.size


class Bike(Vehicle):
    def __init__(self, license_number: str):
        super().__init__(license_number, VehicleSize.SMALL)


class Car(Vehicle):
    def __init__(self, license_number: str):
        super().__init__(license_number, VehicleSize.MEDIUM)

class Truck(Vehicle):
    def __init__(self, license_number: str):
        super().__init__(license_number, VehicleSize.LARGE)

class ParkingSpot:
    def __init__(self, spot_id: str, spot_size: VehicleSize):
        self.spot_id = spot_id
        self.spot_size = spot_size
        self.is_occupied = False
        self.parked_vehicle = None
        self._lock = threading.Lock()

    def get_spot_id(self) -> str:
        return self.spot_id

    def get_spot_size(self) -> VehicleSize:
        return self.spot_size

    def is_available(self) -> bool:
        with self._lock:
            return not self.is_occupied

    def is_occupied_spot(self) -> bool:
        return self.is_occupied

    def park_vehicle(self, vehicle: Vehicle):
        with self._lock:
            self.parked_vehicle = vehicle
            self.is_occupied = True

    def unpark_vehicle(self):
        with self._lock:
            self.parked_vehicle = None
            self.is_occupied = False

    def can_fit_vehicle(self, vehicle: Vehicle) -> bool:
        if self.is_occupied:
            return False

        if vehicle.get_size() == VehicleSize.SMALL:
            return self.spot_size == VehicleSize.SMALL
        elif vehicle.get_size() == VehicleSize.MEDIUM:
            return self.spot_size == VehicleSize.MEDIUM or self.spot_size == VehicleSize.LARGE
        elif vehicle.get_size() == VehicleSize.LARGE:
            return self.spot_size == VehicleSize.LARGE
        else:
            return False

class ParkingFloor:
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self.spots: Dict[str, ParkingSpot] = {}
        self._lock = threading.Lock()

    def add_spot(self, spot: ParkingSpot):
        self.spots[spot.get_spot_id()] = spot

    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        with self._lock:
            available_spots = [
                spot for spot in self.spots.values()
                if not spot.is_occupied_spot() and spot.can_fit_vehicle(vehicle)
            ]
            if available_spots:
                # Sort by spot size (smallest first)
                available_spots.sort(key=lambda x: x.get_spot_size().value)
                return available_spots[0]
            return None

    def display_availability(self):
        print(f"--- Floor {self.floor_number} Availability ---")
        available_counts = defaultdict(int)
        
        for spot in self.spots.values():
            if not spot.is_occupied_spot():
                available_counts[spot.get_spot_size()] += 1

        for size in VehicleSize:
            print(f"  {size.name} spots: {available_counts[size]}")


class ParkingTicket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.entry_timestamp = int(time.time() * 1000)
        self.exit_timestamp = 0

    def get_ticket_id(self) -> str:
        return self.ticket_id

    def get_vehicle(self) -> Vehicle:
        return self.vehicle

    def get_spot(self) -> ParkingSpot:
        return self.spot

    def get_entry_timestamp(self) -> int:
        return self.entry_timestamp

    def get_exit_timestamp(self) -> int:
        return self.exit_timestamp

    def set_exit_timestamp(self):
        self.exit_timestamp = int(time.time() * 1000)


# interface
class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, parking_ticket: ParkingTicket) -> float:
        pass

class FlatRateFeeStrategy(FeeStrategy):
    RATE_PER_HOUR = 10.0

    def calculate_fee(self, parking_ticket: ParkingTicket) -> float:
        duration = parking_ticket.get_exit_timestamp() - parking_ticket.get_entry_timestamp()
        hours = (duration // (1000 * 60 * 60)) + 1
        return hours * self.RATE_PER_HOUR

class VehicleBasedFeeStrategy(FeeStrategy):
    HOURLY_RATES = {
        VehicleSize.SMALL: 10.0,
        VehicleSize.MEDIUM: 20.0,
        VehicleSize.LARGE: 30.0
    }

    def calculate_fee(self, parking_ticket: ParkingTicket) -> float:
        duration = parking_ticket.get_exit_timestamp() - parking_ticket.get_entry_timestamp()
        hours = (duration // (1000 * 60 * 60)) + 1
        return hours * self.HOURLY_RATES[parking_ticket.get_vehicle().get_size()]


# interface
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        pass

class NearestFirstStrategy(ParkingStrategy):
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in floors:
            spot = floor.find_available_spot(vehicle)
            if spot is not None:
                return spot
        return None

class FarthestFirstStrategy(ParkingStrategy):
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        reversed_floors = list(reversed(floors))
        for floor in reversed_floors:
            spot = floor.find_available_spot(vehicle)
            if spot is not None:
                return spot
        return None

class BestFitStrategy(ParkingStrategy):
    def find_spot(self, floors: List[ParkingFloor], vehicle: Vehicle) -> Optional[ParkingSpot]:
        best_spot = None

        for floor in floors:
            spot_on_this_floor = floor.find_available_spot(vehicle)

            if spot_on_this_floor is not None:
                if best_spot is None:
                    best_spot = spot_on_this_floor
                else:
                    # A smaller spot size enum ordinal means a tighter fit
                    if list(VehicleSize).index(spot_on_this_floor.get_spot_size()) < list(VehicleSize).index(best_spot.get_spot_size()):
                        best_spot = spot_on_this_floor

        return best_spot



class ParkingLot:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if ParkingLot._instance is not None:
            raise Exception("This class is a singleton!")
        self.floors: List[ParkingFloor] = []
        self.active_tickets: Dict[str, ParkingTicket] = {}
        self.fee_strategy = FlatRateFeeStrategy()
        self.parking_strategy = NearestFirstStrategy()
        self._main_lock = threading.Lock()

    @staticmethod
    def get_instance():
        if ParkingLot._instance is None:
            with ParkingLot._lock:
                if ParkingLot._instance is None:
                    ParkingLot._instance = ParkingLot()
        return ParkingLot._instance

    def add_floor(self, floor: ParkingFloor):
        self.floors.append(floor)

    def set_fee_strategy(self, fee_strategy: FeeStrategy):
        self.fee_strategy = fee_strategy

    def set_parking_strategy(self, parking_strategy: ParkingStrategy):
        self.parking_strategy = parking_strategy

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        with self._main_lock:
            spot = self.parking_strategy.find_spot(self.floors, vehicle)
            if spot is not None:
                spot.park_vehicle(vehicle)
                ticket = ParkingTicket(vehicle, spot)
                self.active_tickets[vehicle.get_license_number()] = ticket
                print(f"Vehicle {vehicle.get_license_number()} parked at spot {spot.get_spot_id()}")
                return ticket
            else:
                print(f"No available spot for vehicle {vehicle.get_license_number()}")
                return None

    def unpark_vehicle(self, license_number: str) -> Optional[float]:
        with self._main_lock:
            ticket = self.active_tickets.pop(license_number, None)
            if ticket is None:
                print(f"Ticket not found for vehicle {license_number}")
                return None

            ticket.get_spot().unpark_vehicle()
            ticket.set_exit_timestamp()
            fee = self.fee_strategy.calculate_fee(ticket)
            print(f"Vehicle {license_number} unparked from spot {ticket.get_spot().get_spot_id()}")
            return fee


class ParkingLotDemo:
    @staticmethod
    def main():
        parking_lot = ParkingLot.get_instance()

        # 1. Initialize the parking lot with floors and spots
        floor1 = ParkingFloor(1)
        floor1.add_spot(ParkingSpot("F1-S1", VehicleSize.SMALL))
        floor1.add_spot(ParkingSpot("F1-M1", VehicleSize.MEDIUM))
        floor1.add_spot(ParkingSpot("F1-L1", VehicleSize.LARGE))

        floor2 = ParkingFloor(2)
        floor2.add_spot(ParkingSpot("F2-M1", VehicleSize.MEDIUM))
        floor2.add_spot(ParkingSpot("F2-M2", VehicleSize.MEDIUM))

        parking_lot.add_floor(floor1)
        parking_lot.add_floor(floor2)

        parking_lot.set_fee_strategy(VehicleBasedFeeStrategy())

        # 2. Simulate vehicle entries
        print("\n--- Vehicle Entries ---")
        floor1.display_availability()
        floor2.display_availability()

        bike = Bike("B-123")
        car = Car("C-456")
        truck = Truck("T-789")

        bike_ticket = parking_lot.park_vehicle(bike)
        car_ticket = parking_lot.park_vehicle(car)
        truck_ticket = parking_lot.park_vehicle(truck)

        print("\n--- Availability after parking ---")
        floor1.display_availability()
        floor2.display_availability()

        # 3. Simulate another car entry (should go to floor 2)
        car2 = Car("C-999")
        car2_ticket = parking_lot.park_vehicle(car2)

        # 4. Simulate a vehicle entry that fails (no available spots)
        bike2 = Bike("B-000")
        failed_bike_ticket = parking_lot.park_vehicle(bike2)

        # 5. Simulate vehicle exits and fee calculation
        print("\n--- Vehicle Exits ---")

        if car_ticket is not None:
            fee = parking_lot.unpark_vehicle(car.get_license_number())
            if fee is not None:
                print(f"Car C-456 unparked. Fee: ${fee:.2f}")

        print("\n--- Availability after one car leaves ---")
        floor1.display_availability()
        floor2.display_availability()


if __name__ == "__main__":
    ParkingLotDemo.main()

