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

	def getPizza(self):
		return self._basePizza

	def calculateCost(self):
		return self._basePizza.calculateCost()

class ExtraCheese(ToppingDecorator):
	
	_basePizza = None
	
	def __init__(self, basePizza):
		self._basePizza = basePizza
		
	def calculateCost(self):
		return self.getPizza().cost() + 10

