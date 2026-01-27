from abc import ABC, abstractmethod

class BasePizza(ABC):
    @abstractmethod
    def cost(self):
        pass

class Farmhouse(BasePizza):
    def cost(self):
        return 200

class VegDelight(BasePizza):
    def cost(self):
        return 120

class Margheretta(BasePizza):
    def cost(self):
        return 100

class ToppingDecorator(BasePizza, ABC):    
    def __init__(self, base_pizza):
        self.base_pizza = base_pizza

    @abstractmethod
    def cost(self):
        pass

class ExtraCheese(ToppingDecorator):
    def __init__(self, base_pizza):
        super().__init__(base_pizza)
    
    def cost(self):
        return self.base_pizza.cost() + 10

class Mushrooms(ToppingDecorator):
    def __init__(self, base_pizza):
        super().__init__(base_pizza)
    
    def cost(self):
        return self.base_pizza.cost() + 15

if __name__ == '__main__':
    pizza = ExtraCheese(Margheretta())
    print(pizza.cost())

    pizza = Mushrooms(ExtraCheese(Margheretta()))
    print(pizza.cost())
