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
	def get_shape(self, input):
		if input == 'CIRCLE':
			return Circle()
		elif input == 'RECTANGLE':
			return Rectangle()
		else:
			return Square()

if __name__ == '__main__':
	shape_factory_obj = ShapeFactory()
	shape_obj_1 = shape_factory_obj.get_shape('CIRCLE')	# circle object
	shape_obj_2 = shape_factory_obj.get_shape('SQUARE')	# square object

	shape_obj_1.draw()
	shape_obj_2.draw()

