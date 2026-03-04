from abc import ABC, abstractmethod
import uuid
from datetime import date, timedelta


class Car:
    def __init__(self, make, model, year, license_plate, rental_price_per_day):
        self.make = make
        self.model = model
        self.year = year
        self.license_plate = license_plate
        self.rental_price_per_day = rental_price_per_day

    def get_rental_price_per_day(self):
        return self.rental_price_per_day

    def get_license_plate(self):
        return self.license_plate

    def get_make(self):
        return self.make

    def get_model(self):
        return self.model


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class CreditCardPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        # Process credit card payment
        # ...
        print(f"Processing credit card payment of {amount}")
        return True


class PayPalPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        # Process PayPal payment
        # ...
        print(f"Processing paypal payment of {amount}")
        return True


class Customer:
    def __init__(self, name, contact_info, drivers_license_number):
        self.name = name
        self.contact_info = contact_info
        self.drivers_license_number = drivers_license_number


class Reservation:
    def __init__(self, reservation_id, customer, car, start_date, end_date, total_price):
        self.reservation_id = reservation_id
        self.customer = customer
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_car(self):
        return self.car

    def get_total_price(self):
        return self.total_price

    def get_reservation_id(self):
        return self.reservation_id


class RentalSystem:
    def __init__(self, payment_processor: PaymentProcessor):
        self.cars = {}
        self.reservations = {}
        self.payment_processor = payment_processor

    def add_car(self, car):
        self.cars[car.license_plate] = car

    def remove_car(self, license_plate):
        self.cars.pop(license_plate, None)

    def search_cars(self, make=None, model=None, start_date=None, end_date=None):
        result = []
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError("Invalid date range")

        for car in self.cars.values():
            if make and car.make.lower() != make.lower():
                continue

            if model and car.model.lower() != model.lower():
                continue

            if start_date and end_date:
                if not self.is_car_available(car, start_date, end_date):
                    continue

            result.append(car)

        return result

    def is_car_available(self, car, start_date, end_date):
        for reservation in self.reservations.values():
            if reservation.get_car().get_license_plate() == car.get_license_plate():
                # Overlap check
                if not (end_date < reservation.start_date or start_date > reservation.end_date):
                    return False
        return True

    def calculate_price(self, car, start_date, end_date):
        days = (end_date - start_date).days + 1
        return car.get_rental_price_per_day() * days

    def make_reservation(self, customer, car, start_date, end_date):
        if start_date > end_date:
            raise ValueError("Invalid date range")

        if not self.is_car_available(car, start_date, end_date):
            return None

        total_price = self.calculate_price(car, start_date, end_date)

        # Process payment BEFORE confirming
        if not self.process_payment(total_price):
            return None

        reservation_id = self.generate_reservation_id()

        reservation = Reservation(
            reservation_id,
            customer,
            car,
            start_date,
            end_date,
            total_price
        )

        self.reservations[reservation_id] = reservation
        return reservation

    def cancel_reservation(self, reservation_id):
        self.reservations.pop(reservation_id, None)

    def process_payment(self, total_price):
        return self.payment_processor.process_payment(total_price)

    def generate_reservation_id(self):
        return "RES" + str(uuid.uuid4())[:8].upper()



class CarRentalSystemDemo:
    @staticmethod
    def run():
        payment_processor = CreditCardPaymentProcessor()
        rental_system = RentalSystem(payment_processor)

        # Add cars
        rental_system.add_car(Car("Toyota", "Camry", 2022, "ABC123", 50.0))
        rental_system.add_car(Car("Honda", "Civic", 2021, "XYZ789", 45.0))
        rental_system.add_car(Car("Ford", "Mustang", 2023, "DEF456", 80.0))

        # Create customer
        customer = Customer("John Doe", "john@example.com", "DL1234")

        start_date = date.today()
        end_date = start_date + timedelta(days=3)

        # Use search functionality
        available_cars = rental_system.search_cars(
            make="Toyota",
            model="Camry",
            start_date=start_date,
            end_date=end_date
        )

        if available_cars:
            selected_car = available_cars[0]

            reservation = rental_system.make_reservation(
                customer,
                selected_car,
                start_date,
                end_date
            )

            if reservation:
                print("Reservation successful!")
                print(f"Reservation ID: {reservation.get_reservation_id()}")
            else:
                print("Reservation failed (payment issue).")
        else:
            print("No available cars found.")


if __name__ == "__main__":
    CarRentalSystemDemo.run()
