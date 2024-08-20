from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self):
        self.vehicle_id = 0
        self.vehicle_number = 0
        self.vehicle_type = None
        self.company_name = None
        self.model_name = None
        self.km_driven = 0
        self.manufacturing_date = None
        self.average = 0
        self.cc = 0
        self.daily_rental_cost = 0
        self.hourly_rental_cost = 0
        self.no_of_seat = 0
        self.status = None

    def get_vehicle_id(self):
        return self.vehicleID

    def set_vehicle_id(self, vehicleID):
        self.vehicleID = vehicleID

    def get_vehicle_number(self):
        return self.vehicleNumber

    def setVehicleNumber(self, vehicleNumber):
        self.vehicleNumber = vehicleNumber

    def getVehicleType(self):
        return self.vehicleType

    def setVehicleType(self, vehicleType):
        self.vehicleType = vehicleType

    def getCompanyName(self):
        return self.companyName

    def setCompanyName(self, companyName):
        self.companyName = companyName

    def getModelName(self):
        return self.modelName

    def setModelName(self, modelName):
        self.modelName = modelName

    def getKmDriven(self):
        return self.kmDriven

    def setKmDriven(self, kmDriven):
        self.kmDriven = kmDriven

    def getManufacturingDate(self):
        return self.manufacturingDate

    def setManufacturingDate(self, manufacturingDate):
        self.manufacturingDate = manufacturingDate

    def getAverage(self):
        return self.average

    def setAverage(self, average):
        self.average = average

    def getCc(self):
        return self.cc

    def setCc(self, cc):
        self.cc = cc

    def getDailyRentalCost(self):
        return self.dailyRentalCost

    def setDailyRentalCost(self, dailyRentalCost):
        self.dailyRentalCost = dailyRentalCost

    def getHourlyRentalCost(self):
        return self.hourlyRentalCost

    def setHourlyRentalCost(self, hourlyRentalCost):
        self.hourlyRentalCost = hourlyRentalCost

    def getNoOfSeat(self):
        return self.noOfSeat

    def setNoOfSeat(self, noOfSeat):
        self.noOfSeat = noOfSeat

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

class Bike(Vehicle):
    pass

class Car(Vehicle):
    pass

from enum import Enum

class Status(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

class VehicleType(Enum):
    CAR = 'CAR'

class Bill:
    def __init__(self, reservation):
        self.reservation = reservation
        self.totalBillAmount = self.computeBillAmount()
        self.isBillPaid = False

    def computeBillAmount(self):
        return 100.0

class Location:
    def __init__(self, address, pincode, city, state, country):
        self.address = address
        self.pincode = pincode
        self.city = city
        self.state = state
        self.country = country

class Payment:
    def pay_bill(self, bill):
        # do payment processing and update the bill status
        pass

class PaymentDetails:
    def __init__(self):
        self.paymentId = 0
        self.amountPaid = 0
        self.dateOfPayment = None
        self.isRefundable = False
        self.paymentMode = None

class PaymentMode(Enum):
    CASH = 'CASH'
    ONLINE = 'ONLINE'

class Reservation:
    def __init__(self):
        self.reservationId = 0
        self.user = None
        self.vehicle = None
        self.bookingDate = None
        self.dateBookedFrom = None
        self.dateBookedTo = None
        self.fromTimeStamp = 0
        self.toTimeStamp = 0
        self.pickUpLocation = None
        self.dropLocation = None
        self.reservationType = None
        self.reservationStatus = None
        self.location = None
    
    def create_reservation(self, user, vehicle):
        # generate new id
        self.reservationId = 12232
        self.user = user
        self.vehicle = vehicle
        self.reservationType = ReservationType.DAILY
        self.reservationStatus = ReservationStatus.SCHEDULED

        return self.reservationId
    
    # CRUD operations

class ReservationStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    INPROGRESS = 'INPROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

class ReservationType(Enum):
    HOURLY = 'HOURLY'
    DAILY = 'DAILY'

class Store:
    def __init__(self):
        self.storeId = 0
        self.inventoryManagement = None
        self.storeLocation = None
        self.reservations = []

    def getVehicles(self, vehicleType):
        return self.inventoryManagement.getVehicles()

    # addVehicles, update vehicles, use inventory management to update those.

    def setVehicles(self, vehicles):
        self.inventoryManagement = VehicleInventoryManagement(vehicles)

    def createReservation(self, vehicle, user):
        reservation = Reservation()
        reservation.createReserve(user, vehicle)
        self.reservations.append(reservation)
        return reservation

    def completeReservation(self, reservationID):
        # take out the reservation from the list and call complete the reservation method.
        return True

    # update reservation

class User:
    def __init__(self):
        self.userId = 0
        self.userName = 0
        self.drivingLicense = 0

    def getUserId(self):
        return self.userId

    def setUserId(self, userId):
        self.userId = userId
    
    def getUserName(self):
        return self.userName

    def setUserName(self, userName):
        self.userName = userName

    def getDrivingLicense(self):
        return self.drivingLicense

    def setDrivingLicense(self, drivingLicense):
        self.drivingLicense = drivingLicense

class VehicleInventoryManagement:
    def __init__(self, vehicles):
        self.vehicles = vehicles

    def getVehicles(self):
        # filtering
        return self.vehicles

    def setVehicles(self, vehicles):
        self.vehicles = vehicles

class VehicleRentalSystem:
    def __init__(self, stores, users):
        self.storeList = stores
        self.userList = users

    def getStore(self, location):
        # based on location, we will filter out the Store from storeList.
        return self.storeList[0]

    # addUsers

    # remove users

    # add stores

    # remove stores

class Main:
    def main(self):
        users = self.addUsers()
        vehicles = self.addVehicles()
        stores = self.addStores(vehicles)

        rentalSystem = VehicleRentalSystem(stores, users)

        # 0. User comes
        user = users[0]

        # 1. user search store based on location
        location = Location(403012, "Bangalore", "Karnataka", "India")
        store = rentalSystem.getStore(location)

        # 2. get All vehicles you are interested in (based upon different filters)
        storeVehicles = store.getVehicles(VehicleType.CAR)

        # 3.reserving the particular vehicle
        reservation = store.createReservation(storeVehicles[0], users[0])

       # 4. generate the bill
        bill = Bill(reservation)

        # 5. make payment
        payment = Payment()
        payment.payBill(bill)

        # 6. trip completed, submit the vehicle and close the reservation
        store.completeReservation(reservation.reservationId)

    def addVehicles():
        vehicles = []

        vehicle1 = Car()
        vehicle1.setVehicleID(1)
        vehicle1.setVehicleType(VehicleType.CAR)

        vehicle2 = Car()
        vehicle1.setVehicleID(2)
        vehicle1.setVehicleType(VehicleType.CAR)

        vehicles.add(vehicle1)
        vehicles.add(vehicle2)

        return vehicles

    def addUsers():
        users = []
        user1 = User()
        user1.setUserId(1)

        users.add(user1)
        return users

    def addStores(self, vehicles):
        stores = []
        store1 = Store()
        store1.storeId = 1
        store1.setVehicles(vehicles)

        stores.add(store1)
        return stores

if __name__ == '__main__':
    main = Main()
    main.main()

