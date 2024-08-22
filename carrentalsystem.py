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
        return self.vehicle_id

    def set_vehicle_id(self, vehicle_id):
        self.vehicle_id = vehicle_id

    def get_vehicle_number(self):
        return self.vehicle_number

    def set_vehicle_number(self, vehicle_number):
        self.vehicle_number = vehicle_number

    def get_vehicle_type(self):
        return self.vehicle_type

    def set_vehicle_type(self, vehicle_type):
        self.vehicle_type = vehicle_type

    def get_company_name(self):
        return self.company_name

    def set_company_name(self, company_name):
        self.company_name = company_name

    def get_model_name(self):
        return self.model_name

    def set_model_name(self, model_name):
        self.model_name = model_name

    def get_km_driven(self):
        return self.km_driven

    def set_km_driven(self, km_driven):
        self.km_driven = km_driven

    def get_manufacturing_date(self):
        return self.manufacturing_date

    def set_manufacturing_date(self, manufacturing_date):
        self.manufacturing_date = manufacturing_date

    def get_average(self):
        return self.average

    def set_average(self, average):
        self.average = average

    def get_cc(self):
        return self.cc

    def set_cc(self, cc):
        self.cc = cc

    def get_daily_rental_cost(self):
        return self.daily_rental_cost

    def set_daily_rental_cost(self, daily_rental_cost):
        self.daily_rental_cost = daily_rental_cost

    def get_hourly_rental_cost(self):
        return self.hourly_rental_cost

    def set_hourly_rental_cost(self, hourly_rental_cost):
        self.hourly_rental_cost = hourly_rental_cost

    def get_no_of_seat(self):
        return self.no_of_seat

    def set_no_of_seat(self, no_of_seat):
        self.no_of_seat = no_of_seat

    def get_status(self):
        return self.status

    def set_status(self, status):
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
        self.total_bill_amount = self.compute_bill_amount()
        self.is_bill_paid = False

    def compute_bill_amount(self):
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
        self.reservation_id = 0
        self.user = None
        self.vehicle = None
        self.booking_date = None
        self.date_booked_from = None
        self.date_booked_to = None
        self.from_time_stamp = 0
        self.to_time_stamp = 0
        self.pick_up_location = None
        self.drop_location = None
        self.reservation_type = None
        self.reservation_status = None
        self.location = None
    
    def create_reservation(self, user, vehicle):
        # generate new id
        self.reservation_id = 12232
        self.user = user
        self.vehicle = vehicle
        self.reservation_type = ReservationType.DAILY
        self.reservation_status = ReservationStatus.SCHEDULED

        return self.reservation_id
    
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
        self.store_id = 0
        self.inventory_management = None
        self.store_location = None
        self.reservations = []

    def get_vehicles(self, vehicle_type):
        return self.inventory_management.get_vehicles()

    # addVehicles, update vehicles, use inventory management to update those.

    def set_vehicles(self, vehicles):
        self.inventory_management = VehicleInventoryManagement(vehicles)

    def create_reservation(self, vehicle, user):
        reservation = Reservation()
        reservation.create_reserve(user, vehicle)
        self.reservations.append(reservation)
        return reservation

    def complete_reservation(self, reservation_id):
        # take out the reservation from the list and call complete the reservation method.
        return True

    # update reservation

class User:
    def __init__(self):
        self.user_id = 0
        self.user_name = 0
        self.drivingLicense = 0

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id
    
    def get_user_name(self):
        return self.user_name

    def set_user_name(self, user_name):
        self.user_name = user_name

    def get_driving_license(self):
        return self.driving_license

    def set_driving_license(self, driving_license):
        self.driving_license = driving_license

class VehicleInventoryManagement:
    def __init__(self, vehicles):
        self.vehicles = vehicles

    def get_vehicles(self):
        # filtering
        return self.vehicles

    def set_vehicles(self, vehicles):
        self.vehicles = vehicles

class VehicleRentalSystem:
    def __init__(self, stores, users):
        self.store_list = stores
        self.user_list = users

    def get_store(self, location):
        # based on location, we will filter out the Store from storeList.
        return self.store_list[0]

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

