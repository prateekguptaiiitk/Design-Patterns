from abc import ABC, abstractmethod

class Shape(ABC):

	@abstractmethod
	def draw(self):
		pass


class Rectangle(Shape):

	def draw(self):
		print('It is Rectangle')

class Circle(Shape):

	def draw(self):
		print('It is Circle')

class Square(Shape):

	def draw(self):
		print('It is Square')

class ShapeFactory():
	def getShape(self, input):

		if input == 'CIRCLE':
			return Circle()
		elif input == 'RECTANGLE':
			return Rectangle()
		else:
			return Square()


shapeFactoryObj = ShapeFactory()
shapeObj1 = shapeFactoryObj.getShape('CIRCLE')	# circle object
shapeObj2 = shapeFactoryObj.getShape('SQUARE')	# square object

shapeObj1.draw()
shapeObj2.draw()

