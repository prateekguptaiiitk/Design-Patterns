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
		self.floor = floor.floorNumber
		self.direction = direction

	def showDisplay(self):
		print('Current floor: ', self.floor, ' and moving ', self.direction)

class ElevatorCar():
	elevatorID = 0
	display = None
	internalButtons = None
	elevatorState = None
	currentFloor = 0
	elevatorDirection = None
	elevatorDoor = None
	is_empty = True

	def __init__(self, id):
		self.display = ElevatorDisplay()
		self.internalButtons = InternalButtons()
		self.elevatorState = ElevatorState.IDLE
		self.currentFloor = BuildingCreator().floorList[0]
		self.elevatorDirection = Direction.UP
		self.elevatorDoor = ElevatorDoor()
		self.elevatorID = id
		self.is_empty = True

	def showDisplay(self):
		self.display.showDisplay()		

	def moveElevator(self, destinationFloor):
		self.elevatorState = ElevatorState.MOVING
		startFloor = self.currentFloor
		floorList = BuildingCreator().floorList

		if startFloor.floorNumber < destinationFloor:
			self.elevatorDirection = Direction.UP
			for i in range(startFloor.floorNumber, destinationFloor + 1):
				self.currentFloor = floorList[i - 1]
				self.display.setDisplay(self.currentFloor, self.elevatorDirection.name)
				self.showDisplay()

				if self.currentFloor.floorNumber == destinationFloor:
					return True
		else:
			self.elevatorDirection = Direction.DOWN
			for i in range(startFloor.floorNumber, destinationFloor - 1, -1):
				self.currentFloor = floorList[i - 1]
				self.display.setDisplay(self.currentFloor, self.elevatorDirection.name)
				self.showDisplay()

				if self.currentFloor.floorNumber == destinationFloor:
					return True

		return False

from collections import deque
class ElevatorController():
	requestQueue = deque()
	elevatorCar = None

	def __init__(self, elevatorCar):
		self.elevatorCar = elevatorCar

	def submitNewRequest(self, currFloor):
		self.requestQueue.append(currFloor)
		self.controlElevator()

	def controlElevator(self):
		elevatorDoor = ElevatorDoor()
		while self.requestQueue:
			destinationFloor = self.requestQueue.popleft()
			status = self.elevatorCar.moveElevator(destinationFloor)
			if status:
				elevatorDoor.openDoor()
				elevatorDoor.closeDoor()

				if not self.elevatorCar.is_empty:
					destFloor = int(input('Enter your destination floor number: '))
					InternalButtons().pressButton(destFloor, self.elevatorCar)

class InternalButtons():
	dispatcher = None
	availableButtons = None

	def __init__(self):
		self.availableButtons = []

	def pressButton(self, destination, elevatorCar):
		# 1. check if destination is in the list of available floors
		floorList = BuildingCreator().floorList
		for i in range(1, len(floorList)):
			if elevatorCar.elevatorID % 2 == i % 2:
				self.availableButtons.append(i)

		if destination not in self.availableButtons:
			print('Incorrect destination floor number entered')
			return
		
		# 2. submit the request to the jobDispatcher
		dispatcher = InternalButtonDispatcher()
		dispatcher.submitInternalRequest(destination, elevatorCar)

class InternalButtonDispatcher():

	def __init__(self):
		self.elevatorControllerList = ElevatorCreator().elevatorControllerList

	def submitInternalRequest(self, currFloor, elevatorCar):
		# for simplicity we are following even odd
		for elevatorController in self.elevatorControllerList:
			elevatorID = elevatorController.elevatorCar.elevatorID

			if elevatorID == elevatorCar.elevatorID:
				elevatorController.elevatorCar.is_empty = True
				elevatorController.submitNewRequest(currFloor)

class ExternalButtons():
	dispatcher = None

	def __init__(self):
		self.dispatcher = ExternalButtonDispatcher()

	def pressButton(self, currFloor):
		# Submit the request to the job dispatcher
		self.dispatcher.submitExternalRequest(currFloor)

class ExternalButtonDispatcher():
	elevatorControllerList = None

	def __init__(self):
		self.elevatorControllerList = ElevatorCreator().elevatorControllerList

	def submitExternalRequest(self, currFloor):
		# for simplicity we are following even odd
		for elevatorController in self.elevatorControllerList:
			elevatorID = elevatorController.elevatorCar.elevatorID

			if elevatorID % 2 == currFloor % 2:
				elevatorController.elevatorCar.is_empty = False
				elevatorController.submitNewRequest(currFloor)

class ElevatorDoor():
	def openDoor(self):
		print('Opening the Elevator door')

	def closeDoor(self):
		print('Closing the Elevator door')

class Floor():
	floorNumber = 0

	def __init__(self, floorNumber):
		self.floorNumber = floorNumber

class Building():
	floorList = None

	def __init__(self):
		self.floorList = []

	def addFloor(self, newFloor):
		self.floorList.append(newFloor)

	def removeFloor(self, removeFloor):
		self.floorList.remove(removeFloor)

	def getAllFloorList(self):
		return self.floorList
	
class BuildingCreator():
	building = Building()

	for i in range(1, 11):
		floor = Floor(i)
		building.addFloor(floor)

	floorList = building.getAllFloorList()

class ElevatorCreator():
	elevatorControllerList = []
	
	elevatorCar1 = ElevatorCar(1)
	controller1 = ElevatorController(elevatorCar1)

	elevatorCar2 = ElevatorCar(2)
	controller2 = ElevatorController(elevatorCar2)

	elevatorControllerList.append(controller1)
	elevatorControllerList.append(controller2)

if __name__ == '__main__':
	
	buildingCreator = BuildingCreator()

	elevatorCreator = ElevatorCreator()
	externalButton = ExternalButtons()

	floorReq = int(input('Enter your current floor number: '))
	dirReq = input('Enter direction(UP or DOWN): ')
	destDir = Direction.UP if dirReq == 'UP' else Direction.DOWN
	externalButton.pressButton(floorReq)

	floorReq = int(input('Enter your current floor number: '))
	dirReq = input('Enter direction(UP or DOWN): ')
	destDir = Direction.UP if dirReq == 'UP' else Direction.DOWN
	externalButton.pressButton(floorReq)





