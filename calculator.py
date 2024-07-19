from enum import Enum
class Operation(Enum):
    ADD = 'ADD'
    SUBTRACT = 'SUBTRACT'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'

from abc import ABC, abstractmethod
class ArithmeticExpression(ABC):
    @abstractmethod
    def evaluate(self):
        pass

class Expression(ArithmeticExpression):
    leftExpression = None
    rightExpression = None
    operation = None

    def __init__(self, leftPart, rightPart, operation):
        self.leftExpression = leftPart
        self.rightExpression = rightPart
        self.operation = operation

    def evaluate(self):
        value = 0
        if self.operation == Operation.ADD:
            value = self.leftExpression.evaluate() + self.rightExpression.evaluate()
        elif self.operation == Operation.SUBTRACT:
            value = self.leftExpression.evaluate() - self.rightExpression.evaluate()
        elif self.operation == Operation.DIVIDE:
            value = self.leftExpression.evaluate() / self.rightExpression.evaluate()
        elif self.operation == Operation.MULTIPLY:
            value = self.leftExpression.evaluate() * self.rightExpression.evaluate()

        print("Expression value is :", value)
        return value

class ArithmenticNumber(ArithmeticExpression):
    value = 0

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        print("Number value is :", self.value)
        return self.value

if __name__ == '__main__':
    '''
        2*(1+7)

          *
        /   \
       2     +
            / \
           1   7

    '''

    two = ArithmenticNumber(2)
    one = ArithmenticNumber(1)
    seven = ArithmenticNumber(7)

    addExpression = Expression(one,seven, Operation.ADD)
    parentExpression = Expression(two,addExpression, Operation.MULTIPLY)

    print('Final result: ', parentExpression.evaluate())

