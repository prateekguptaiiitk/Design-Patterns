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
	elevatorID = 0
	display = None
	internalButtons = None
	elevatorState = None
	currentFloor = 0
	elevatorDirection = None
	elevatorDoor = None

	def __init__(self, id):
		self.display = ElevatorDisplay()
		self.internalButtons = InternalButtons()
		self.elevatorState = ElevatorState.IDLE
		self.currentFloor = 0
		self.elevatorDirection = Direction.UP
		self.elevatorDoor = ElevatorDoor()
		self.elevatorID = id

	def showDisplay(self):
		self.display.showDisplay()		

	def moveElevator(self, dir, destinationFloor):
		startFloor = self.currentFloor

		if startFloor < destinationFloor:
			self.elevatorDirection = Direction.UP
			for i in range(startFloor, destinationFloor + 1):
				self.currentFloor = i
				self.display.setDisplay(self.currentFloor, self.elevatorDirection.name)
				self.showDisplay()

				if i == destinationFloor:
					return True
		else:
			self.elevatorDirection = Direction.DOWN
			for i in range(startFloor, destinationFloor - 1, -1):
				self.currentFloor = i
				self.display.setDisplay(self.currentFloor, self.elevatorDirection.name)
				self.showDisplay()

				if i == destinationFloor:
					return True

		return False

from collections import deque
class ElevatorController():
	requestQueue = deque()
	elevatorCar = None

	def __init__(self, elevatorCar):
		self.elevatorCar = elevatorCar

	def submitNewRequest(self, currFloor, direction):
		self.requestQueue.append((currFloor, direction))
		self.controlElevator()

	# def submitInternalRequest(self, floor):
	# 	pass

	def controlElevator(self):
		elevatorDoor = ElevatorDoor()
		while self.requestQueue:
			req = self.requestQueue.popleft()
			status = self.elevatorCar.moveElevator(req[1], req[0])
			if status:
				elevatorDoor.openDoor()
				elevatorDoor.closeDoor()

				# destFloor = int(input('Enter destination floor no. you want to go'))
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
			elevatorID = elevatorController.elevatorCar.elevatorID

			if elevatorID % 2 == currFloor % 2:
				elevatorController.submitNewRequest(currFloor, direction)

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
	
	elevatorCar1 = ElevatorCar(1)
	controller1 = ElevatorController(elevatorCar1)

	elevatorCar2 = ElevatorCar(2)
	controller2 = ElevatorController(elevatorCar2)

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
	externalButton = ExternalButtons()

	floorReq = int(input('Enter your current floor number: '))
	dirReq = input('Enter direction(UP or DOWN): ')
	destDir = Direction.UP if dirReq == 'UP' else Direction.DOWN
	externalButton.pressButton(floorReq, destDir)

	floorReq = int(input('Enter your current floor number: '))
	dirReq = input('Enter direction(UP or DOWN): ')
	destDir = Direction.UP if dirReq == 'UP' else Direction.DOWN
	externalButton.pressButton(floorReq, destDir)





