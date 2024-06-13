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

class ToppingDecorator(BasePizza):

	_basePizza = None
	
	def __init__(self, basePizza):
		self._basePizza = basePizza

	def getBasePizzaCost(self):
		return self._basePizza.cost()

	def cost(self):
		pass


class ExtraCheese(ToppingDecorator):

	def __init__(self, basePizza):
		super().__init__(basePizza)
	
	def cost(self):
		return self.getBasePizzaCost() + 10


class Mushrooms(ToppingDecorator):

	def __init__(self, basePizza):
		super().__init__(basePizza)
	
	def cost(self):
		return self.getBasePizzaCost() + 15

BasePizza = ExtraCheese(Margheretta())
print(BasePizza.cost())

BasePizza = Mushrooms(ExtraCheese(Margheretta()))
print(BasePizza.cost())
