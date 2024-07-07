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
		print(self.floor)
		print(self.direction)

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

	def pressButton(self, destination):
		internalButtons.pressButton(destination)

	def setDisplay(self):
		self.display.setDisplay(self.currentFloor, self.elevatorDirection)

	def moveElevator(self, dir, destinationFloor):
		startFloor = self.currentFloor

		if dir == Direction.UP:
			for i in range(startFloor, destinationFloor + 1):
				self.currentFloor = startFloor
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

import heapq
class ElevatorController():
	upMinPQ = []
	downMaxPQ = []
	elevatorCar = None

	def __init__(self, elevatorCar):
		self.elevatorCar = elevatorCar
		heapq.heapify(self.upMinPQ)
		heapq.heapify(self.downMaxPQ)

	def submitNewRequest(self, floor, direction):
		if direction == Direction.DOWN:
			heapq.heappush(self.downMaxPQ, -floor)
		else:
			heapq.heappush(self.upMinPQ, floor)

	# def submitInternalRequest(self, floor):
	# 	pass

	def controlElevator(self):
		while True:
			if elevatorCar.elevatorDirection == Direction.UP:
				pass

class InternalButtons():
	dispatcher = InternalButtonsDispatcher()
	availableButtons = [1,2,3,4,5,6,7,8,9,10]
	buttonSelected = 0

	def pressButton(self, destination, elevatorCar):
		# 1. check if destination is in the list of available floors
		if destination not in availableButtons:
			print('Incorrect destination floor number entered')
			return

		# 2. submit the request to the jobDispatcher
		dispatcher.submitInternalRequest(destination, elevatorCar)

class InternalButtonsDispatcher():
	elevatorControllerList = ElevatorCreator.elevatorControllerList

	def submitInternalRequest(self, floor, elevatorCar):
		# for simplicity we are following even odd
		for elevatorController in self.elevatorControllerList:
			elevatorID = elevatorController.elevatorCar.id

			if elevatorID % 2 == floor % 2:
				elevatorController.submitNewRequest(floor, direction)

class ExternalButtons():
	dispatcher = ExternalButtonsDispatcher()
	availableButtons = [1,2,3,4,5,6,7,8,9,10]
	buttonSelected = 0

	def pressButton(self, destination, elevatorCar):
		# 1. check if destination is in the list of available floors
		if destination not in availableButtons:
			print('Incorrect destination floor number entered')
			return

		# 2. submit the request to the jobDispatcher
		dispatcher.submitExternalRequest(destination, elevatorCar)

class ExternalButtonDispatcher():
	elevatorControllerList = ElevatorCreator.elevatorControllerList

	def submitExternalRequest(self, floor):
		# for simplicity we are following even odd
		for elevatorController in self.elevatorControllerList:
			elevatorID = elevatorController.elevatorCar.id

			if elevatorID % 2 == floor % 2:
				elevatorController.submitNewRequest(floor, direction)

class ElevatorDoor():
	def openDoor(self):
		print('Opeining the Elevator door')

	def closeDoor(self):
		print('Closing the Elevator door')

class Floor():
	floorNumber = 0
	externalbuttonDispatcher = None

	def __init__(self, floorNumber):
		self.floorNumber = floorNumber
		externalbuttonDispatcher = ExternalbuttonDispatcher()

	def pressButton(self, direction):
		externalbuttonDispatcher.submitExternalRequest(self.floorNumber, direction)

class Building():
	floorList = None

	def __init__(self, floors):
		self.floorList floors

	def addFloors(self, newFloor):
		self.floorList.append(newFloor)

	def removeFloor(self, removeFloor):
		self.floorList.remove(removeFloor)

	def getAllFloorList(self):
		return self.floorList

class ElevatorCreater():
	elevatorControllerList = []

	elevatorCar1 = ElevatorCar()
	elevatorCar1.id = 1
	controller1 = elevatorController(elevatorCar1)

	elevatorCar2 = ElevatorCar()
	elevatorCar2.id = 2
	controller2 = elevatorController(elevatorCar2)

	elevatorControllerList.append(controller1)
	elevatorControllerList.append(controller2)

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






