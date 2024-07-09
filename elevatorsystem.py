from enum import Enum

class Direction(Enum):
	UP = 'UP'
	DOWN = 'DOWN'

class ElevatorState(Enum):
	MOVING = 'MOVING'
	IDLE = 'IDLE'

class ElevatorDisplay():
	floor = 0
	direction = None

	def setDisplay(self, floor, direction):
		self.floor = floor
		self.direction = direction

	def showDisplay(self):
		print('Current floor: ', self.floor, ' and moving ', self.direction)

class ElevatorCar():
	id = 0
	display = None
	internalButtons = None
	elevatorState = None
	currentFloor = 0
	elevatorDirection = None
	elevatorDoor = None

	def __init__(self):
		self.display = ElevatorDisplay()
		self.internalButtons = InternalButtons()
		self.elevatorState = ElevatorState.IDLE
		self.currentFloor = 0
		self.elevatorDirection = Direction.UP
		self.elevatorDoor = ElevatorDoor()

	def showDisplay(self):
		self.display.showDisplay()

	def setDisplay(self):
		self.display.setDisplay(self.currentFloor, self.elevatorDirection.name)

	def moveElevator(self, dir, destinationFloor):
		startFloor = self.currentFloor

		if dir == Direction.UP:
			for i in range(startFloor, destinationFloor + 1):
				self.currentFloor = i
				self.setDisplay()
				self.showDisplay()

				if i == destinationFloor:
					return True

		if dir == Direction.DOWN:
			for i in range(destinationFloor, startFloor - 1, -1):
				self.currentFloor = startFloor
				self.setDisplay()
				self.showDisplay()

				if i == destinationFloor:
					return True

		return False

from collections import deque
class ElevatorController():
	requestQueue = []
	elevatorCar = None

	def __init__(self, elevatorCar):
		self.elevatorCar = elevatorCar
		self.requestQueue = deque()

	def submitNewRequest(self, currFloor, direction):
		self.requestQueue.append((currFloor, direction))
		self.controlElevator()

	# def submitInternalRequest(self, floor):
	# 	pass

	def controlElevator(self):
		while self.requestQueue:
			req = self.requestQueue.popleft()
			status = self.elevatorCar.moveElevator(req[1], req[0])
			if status:
				ElevatorDoor().openDoor()
				ElevatorDoor().closeDoor()

				destFloor = int(input('Enter destination floor no. you want to go'))
				# InternalButtons().pressButton(destFloor)

class InternalButtons():
	availableButtons = None
	buttonSelected = 0

	def __init__(self):
		self.availableButtons = [1,2,3,4,5,6,7,8,9,10]

	def pressButton(self, destination, elevatorCar):
		# 1. check if destination is in the list of available floors
		if destination not in self.availableButtons:
			print('Incorrect destination floor number entered')
			return
		
		# 2. submit the request to the jobDispatcher
		dispatcher = InternalButtonDispatcher()
		dispatcher.submitInternalRequest(destination, elevatorCar)

class InternalButtonDispatcher():
	elevatorControllerList = None

	def __init__(self):
		self.elevatorControllerList = ElevatorCreator().elevatorControllerList

	def submitInternalRequest(self, floor, elevatorCar):
		# for simplicity we are following even odd
		for elevatorController in self.elevatorControllerList:
			elevatorID = elevatorController.elevatorCar.id

			if elevatorID % 2 == floor % 2:
				elevatorController.submitNewRequest(floor)

class ExternalButtons():
	dispatcher = None
	availableButtons = None
	buttonSelected = 0

	def __init__(self):
		self.dispatcher = ExternalButtonDispatcher()
		self.availableButtons = [1,2,3,4,5,6,7,8,9,10]

	def pressButton(self, currFloor, direction):
		# Submit the request to the job dispatcher
		self.dispatcher.submitExternalRequest(currFloor, direction)

class ExternalButtonDispatcher():
	elevatorControllerList = None

	def __init__(self):
		self.elevatorControllerList = ElevatorCreator().elevatorControllerList

	def submitExternalRequest(self, currFloor, direction):
		# for simplicity we are following even odd
		for elevatorController in self.elevatorControllerList:
			elevatorID = elevatorController.elevatorCar.id

			if elevatorID % 2 == currFloor % 2:
				elevatorController.submitNewRequest(currFloor, direction)

class ElevatorDoor():
	def openDoor(self):
		print('Opeining the Elevator door')

	def closeDoor(self):
		print('Closing the Elevator door')

class Floor():
	floorNumber = 0

	def __init__(self, floorNumber):
		self.floorNumber = floorNumber

class Building():
	floorList = None

	def __init__(self, floors):
		self.floorList = floors

	def addFloors(self, newFloor):
		self.floorList.append(newFloor)

	def removeFloor(self, removeFloor):
		self.floorList.remove(removeFloor)

	def getAllFloorList(self):
		return self.floorList

class ElevatorCreator():
	elevatorControllerList = []

	def __init__(self):
		elevatorCar1 = ElevatorCar()
		elevatorCar1.id = 1
		controller1 = ElevatorController(elevatorCar1)

		elevatorCar2 = ElevatorCar()
		elevatorCar2.id = 2
		controller2 = ElevatorController(elevatorCar2)

		self.elevatorControllerList.append(controller1)
		self.elevatorControllerList.append(controller2)

if __name__ == '__main__':
	floorList = []
	floor1 = Floor(1)
	floor2 = Floor(2)
	floor3 = Floor(3)
	floor4 = Floor(4)
	floor5 = Floor(5)

	floorList.append(floor1)
	floorList.append(floor2)
	floorList.append(floor3)
	floorList.append(floor4)
	floorList.append(floor5)

	building = Building(floorList)

	elevatorCreater = ElevatorCreator()

	req1 = int(input('Enter your current floor no.'))
	ExternalButtons().pressButton(req1, Direction.UP)






