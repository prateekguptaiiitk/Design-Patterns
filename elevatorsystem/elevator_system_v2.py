from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Optional, Set
import threading
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import sys


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class RequestSource(Enum):
    INTERNAL = "INTERNAL"  # From inside the cabin
    EXTERNAL = "EXTERNAL"  # From the hall/floor


class Floor:
    def __init__(self, floor_number: int, elevator_system):
        self.floor_number = floor_number
        self.elevator_system = elevator_system
        self.up_button_pressed = False
        self.down_button_pressed = False

    def press_up_button(self):
        print(f"\n[Floor {self.floor_number}] UP button pressed")
        self.up_button_pressed = True
        self.elevator_system.request_elevator(self.floor_number, Direction.UP)

    def press_down_button(self):
        print(f"\n[Floor {self.floor_number}] DOWN button pressed")
        self.down_button_pressed = True
        self.elevator_system.request_elevator(self.floor_number, Direction.DOWN)

    def get_floor_number(self):
        return self.floor_number
    

@dataclass
class Request:
    target_floor: int
    direction: Direction  # Primarily for External requests
    source: RequestSource

    def __str__(self):
        if self.source == RequestSource.EXTERNAL:
            return f"{self.source.value} Request to floor {self.target_floor} going {self.direction.value}"
        else:
            return f"{self.source.value} Request to floor {self.target_floor}"


class ElevatorObserver(ABC):
    @abstractmethod
    def update(self, elevator):
        pass


class ElevatorDisplay(ElevatorObserver):
    def update(self, elevator):
        print(f"[DISPLAY] Elevator {elevator.get_id()} | Current Floor: {elevator.get_current_floor()} | Direction: {elevator.get_direction().value}")


class ElevatorSelectionStrategy(ABC):
    @abstractmethod
    def select_elevator(self, elevators: List, request: Request) -> Optional:
        pass

class NearestElevatorStrategy(ElevatorSelectionStrategy):
    def select_elevator(self, elevators: List, request: Request) -> Optional:
        best_elevator = None
        min_distance = float('inf')

        for elevator in elevators:
            if self._is_suitable(elevator, request):
                distance = abs(elevator.get_current_floor() - request.target_floor)
                if distance < min_distance:
                    min_distance = distance
                    best_elevator = elevator

        return best_elevator

    def _is_suitable(self, elevator, request: Request) -> bool:
        if elevator.get_direction() == Direction.IDLE:
            return True
        if elevator.get_direction() == request.direction:
            if request.direction == Direction.UP and elevator.get_current_floor() <= request.target_floor:
                return True
            if request.direction == Direction.DOWN and elevator.get_current_floor() >= request.target_floor:
                return True
        return False


class ElevatorState(ABC):
    @abstractmethod
    def move(self, elevator):
        pass

    @abstractmethod
    def add_request(self, elevator, request: Request):
        pass

    @abstractmethod
    def get_direction(self) -> Direction:
        pass

class IdleState(ElevatorState):
    def move(self, elevator):
        if elevator.get_up_requests():
            elevator.set_state(MovingUpState())
        elif elevator.get_down_requests():
            elevator.set_state(MovingDownState())
        # Else stay idle

    def add_request(self, elevator, request: Request):
        if request.target_floor > elevator.get_current_floor():
            elevator.get_up_requests().add(request.target_floor)
        elif request.target_floor < elevator.get_current_floor():
            elevator.get_down_requests().add(request.target_floor)
        # If request is for current floor, doors would open (handled implicitly by moving to that floor)

    def get_direction(self) -> Direction:
        return Direction.IDLE
    
class MovingUpState(ElevatorState):
    def move(self, elevator):
        if not elevator.get_up_requests():
            elevator.set_state(IdleState())
            return

        next_floor = min(elevator.get_up_requests())
        elevator.set_current_floor(elevator.get_current_floor() + 1)

        if elevator.get_current_floor() == next_floor:
            print(f"Elevator {elevator.get_id()} stopped at floor {next_floor}")
            elevator.get_up_requests().remove(next_floor)

        if not elevator.get_up_requests():
            elevator.set_state(IdleState())

    def add_request(self, elevator, request: Request):
        # Internal requests always get added to the appropriate queue
        if request.source == RequestSource.INTERNAL:
            if request.target_floor > elevator.get_current_floor():
                elevator.get_up_requests().add(request.target_floor)
            else:
                elevator.get_down_requests().add(request.target_floor)
            return

        # External requests
        if request.direction == Direction.UP and request.target_floor >= elevator.get_current_floor():
            elevator.get_up_requests().add(request.target_floor)
        elif request.direction == Direction.DOWN:
            elevator.get_down_requests().add(request.target_floor)

    def get_direction(self) -> Direction:
        return Direction.UP
    
class MovingDownState(ElevatorState):
    def move(self, elevator):
        if not elevator.get_down_requests():
            elevator.set_state(IdleState())
            return

        next_floor = max(elevator.get_down_requests())
        elevator.set_current_floor(elevator.get_current_floor() - 1)

        if elevator.get_current_floor() == next_floor:
            print(f"Elevator {elevator.get_id()} stopped at floor {next_floor}")
            elevator.get_down_requests().remove(next_floor)

        if not elevator.get_down_requests():
            elevator.set_state(IdleState())

    def add_request(self, elevator, request: Request):
        # Internal requests always get added to the appropriate queue
        if request.source == RequestSource.INTERNAL:
            if request.target_floor > elevator.get_current_floor():
                elevator.get_up_requests().add(request.target_floor)
            else:
                elevator.get_down_requests().add(request.target_floor)
            return

        # External requests
        if request.direction == Direction.DOWN and request.target_floor <= elevator.get_current_floor():
            elevator.get_down_requests().add(request.target_floor)
        elif request.direction == Direction.UP:
            elevator.get_up_requests().add(request.target_floor)

    def get_direction(self) -> Direction:
        return Direction.DOWN


class Elevator:
    def __init__(self, elevator_id: int):
        self.id = elevator_id
        self.current_floor = 1
        self.current_floor_lock = threading.Lock()
        self.state = IdleState()
        self.is_running = True
        
        self.up_requests = set()
        self.down_requests = set()
        
        # Observer Pattern: List of observers
        self.observers = []

    # --- Observer Pattern Methods ---
    def add_observer(self, observer: ElevatorObserver):
        self.observers.append(observer)
        observer.update(self)  # Send initial state

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    # --- State Pattern Methods ---
    def set_state(self, state: ElevatorState):
        self.state = state
        self.notify_observers()  # Notify observers on direction change

    def move(self):
        self.state.move(self)

    # --- Request Handling ---
    def add_request(self, request: Request):
        print(f"Elevator {self.id} processing: {request}")
        self.state.add_request(self, request)

    # --- Getters and Setters ---
    def get_id(self) -> int:
        return self.id

    def get_current_floor(self) -> int:
        with self.current_floor_lock:
            return self.current_floor

    def set_current_floor(self, floor: int):
        with self.current_floor_lock:
            self.current_floor = floor
        self.notify_observers()  # Notify observers on floor change

    def get_direction(self) -> Direction:
        return self.state.get_direction()

    def get_up_requests(self) -> Set[int]:
        return self.up_requests

    def get_down_requests(self) -> Set[int]:
        return self.down_requests

    def is_elevator_running(self) -> bool:
        return self.is_running

    def stop_elevator(self):
        self.is_running = False

    def run(self):
        while self.is_running:
            self.move()
            try:
                time.sleep(1)  # Simulate movement time
            except KeyboardInterrupt:
                self.is_running = False
                break



class ElevatorSystem:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, num_elevators: int, num_floors: int):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, num_elevators: int, num_floors: int):
        if self._initialized:
            return
        
        self.floors = {}

        for floor in range(1, num_floors + 1):
            self.floors[floor] = Floor(floor, self)
        
        self.selection_strategy = NearestElevatorStrategy()
        self.executor_service = ThreadPoolExecutor(max_workers=num_elevators)
        
        elevator_list = []
        display = ElevatorDisplay()  # Create the observer

        for i in range(1, num_elevators + 1):
            elevator = Elevator(i)
            elevator.add_observer(display)  # Attach the observer
            elevator_list.append(elevator)

        self.elevators = {elevator.get_id(): elevator for elevator in elevator_list}
        self._initialized = True

    @classmethod
    def get_instance(cls, num_elevators: int, num_floors: int):
        return cls(num_elevators, num_floors)
    
    def get_floor(self, floor_number: int) -> Optional[Floor]:
        return self.floors.get(floor_number)
    
    def start(self):
        for elevator in self.elevators.values():
            self.executor_service.submit(elevator.run)

    # --- Facade Methods ---

    # EXTERNAL Request (Hall Call)
    def request_elevator(self, floor: int, direction: Direction):
        print(f"\n>> EXTERNAL Request: User at floor {floor} wants to go {direction.value}")
        request = Request(floor, direction, RequestSource.EXTERNAL)

        # Use strategy to find the best elevator
        selected_elevator = self.selection_strategy.select_elevator(list(self.elevators.values()), request)

        if selected_elevator:
            selected_elevator.add_request(request)
        else:
            print("System busy, please wait.")

    # INTERNAL Request (Cabin Call)
    def select_floor(self, elevator_id: int, destination_floor: int):
        print(f"\n>> INTERNAL Request: User in Elevator {elevator_id} selected floor {destination_floor}")
        request = Request(destination_floor, Direction.IDLE, RequestSource.INTERNAL)

        elevator = self.elevators.get(elevator_id)
        if elevator:
            elevator.add_request(request)
        else:
            print("Invalid elevator ID.", file=sys.stderr)

    def shutdown(self):
        print("Shutting down elevator system...")
        for elevator in self.elevators.values():
            elevator.stop_elevator()
        self.executor_service.shutdown()



class ElevatorSystemDemo:
    @staticmethod
    def main():
        import sys
        
        # Setup: A building with 2 elevators
        num_elevators = 2
        num_floors = 10
        # The get_instance method now initializes the elevators and attaches the Display (Observer).
        elevator_system = ElevatorSystem.get_instance(num_elevators, num_floors)


        # Start the elevator system
        elevator_system.start()
        print("Elevator system started. ConsoleDisplay is observing.\n")

        # --- SIMULATION START ---

        # 1. External Request: User at floor 5 wants to go UP.
        # The system will dispatch this to the nearest elevator (likely E1 or E2, both at floor 1).
        elevator_system.get_floor(5).press_up_button()
        time.sleep(0.1)  # Wait for the elevator to start moving

        # 2. Internal Request: Assume E1 took the previous request.
        # The user gets in at floor 5 and presses 10.
        # We send this request directly to E1.

        # Note: In a real simulation, we'd wait until E1 reaches floor 5, but for this demo,
        # we simulate the internal button press shortly after the external one.
        elevator_system.select_floor(1, 10)
        time.sleep(0.2)

        # 3. External Request: User at floor 3 wants to go DOWN.
        # E2 (likely still idle at floor 1) might take this, or E1 if it's convenient.
        elevator_system.get_floor(3).press_down_button()
        time.sleep(0.3)

        # 4. Internal Request: User in E2 presses 1.
        elevator_system.select_floor(2, 1)

        # Let the simulation run for a while to observe the display updates
        print("\n--- Letting simulation run for 1 second ---")
        time.sleep(1)

        # Shutdown the system
        elevator_system.shutdown()
        print("\n--- SIMULATION END ---")

if __name__ == "__main__":
    ElevatorSystemDemo.main()
