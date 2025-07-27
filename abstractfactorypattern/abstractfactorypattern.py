class AbstractFactoryProducer:
    def get_factory_instance(self, value):
        if value == 'Economic':
            return EconomicCarFactory()
        elif value == 'luxury' or value == 'Premium':
            return LuxuryCarFactory()
        
        return None

from abc import ABC, abstractmethod

class AbstractFactory(ABC):
    @abstractmethod
    def get_instance(self, price):
        pass

class EconomicCarFactory(AbstractFactory):
    def get_instance(self, price):
        if price <= 300000:
            return EconomicCar1()
        else:
            return EconomicCar2()

class LuxuryCarFactory(AbstractFactory):
    def get_instance(self, price):
        if price >= 1000000 and price <= 2000000:
            return LuxuryCar1()
        elif price > 2000000:
            return LuxuryCar2()
        return None

class Car(ABC):
    def get_top_speed(self):
        pass

class EconomicCar1(Car):
    def get_top_speed(self):
        return 100

class EconomicCar2(Car):
    def get_top_speed(self):
        return 150

class LuxuryCar1(Car):
    def get_top_speed(self):
        return 200

class LuxuryCar2(Car):
    def get_top_speed(self):
        return 250

if __name__ == '__main__':
    abstract_factory_producer_obj = AbstractFactoryProducer()
    abstract_factory_obj = abstract_factory_producer_obj.get_factory_instance('Premium')

    car_obj = abstract_factory_obj.get_instance(5000000)
    print(car_obj.get_top_speed())