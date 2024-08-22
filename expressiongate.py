# from enum import Enum

# class Operator(Enum):
#     AND = 'and'
#     OR = 'or'
#     EQUAL = '=='
#     NOT_EQUAL = '!='
#     LESS_THAN = '<'
#     GREATER_THAN = '>'
#     LESS_THAN_OR_EQUAL = '<='
#     GREATER_THAN_OR_EQUAL = '>='

# from abc import ABC, abstractmethod

# class ExpressionComponent(ABC):
#     @abstractmethod
#     def evaluate(self, variables):
#         pass

# class Expression(ExpressionComponent):
#     def __init__(self, left_part, right_part, operation):
#         self.left_expression = left_part
#         self.right_expression = right_part
#         self.operation = operation

#     def evaluate(self, variables):
#         value = None
#         if self.operation == Operator.AND:
#             value = self.left_expression.evaluate() and self.right_expression.evaluate()
#         elif self.operation == Operator.OR:
#             value = self.left_expression.evaluate() or self.right_expression.evaluate()
#         elif self.operation == Operator.EQUAL:
#             value = self.left_expression.evaluate() == self.right_expression.evaluate()
#         elif self.operation == Operator.NOT_EQUAL:
#             value = self.left_expression.evaluate() != self.right_expression.evaluate()
#         elif self.operation == Operator.LESS_THAN:
#             value = self.left_expression.evaluate() < self.right_expression.evaluate()
#         elif self.operation == Operator.GREATER_THAN:
#             value = self.left_expression.evaluate() > self.right_expression.evaluate()
#         elif self.operation == Operator.LESS_THAN_OR_EQUAL:
#             value = self.left_expression.evaluate() <= self.right_expression.evaluate()
#         elif self.operation == Operator.GREATER_THAN_OR_EQUAL:
#             value = self.left_expression.evaluate() >= self.right_expression.evaluate()

#         print("Expression value is:", value)
#         return value

# class Variable(ExpressionComponent):
#     def __init__(self, name):
#         self.name = name

#     def evaluate(self, variables):
#         return variables[self.name]

# class Literal(ExpressionComponent):
#     def __init__(self, value):
#         self.value = value

#     def evaluate(self, variables):
#         return self.value

# # if __name__ == '__main__':
# #     variables = {
# #         "age": 36,
# #         "location": "Boston",
# #         "name": "Bob"
# #     }

# #     name_var = Variable("name", variables)
# #     location_var = Variable("location", variables)
# #     age_var = Variable("age", variables)

# #     # Logical Expression: name == "Bob" && age <= 45 && location != "NY"
# #     equals_expr = Expression(name_var, Variable("Bob", {}), Operator.EQUAL)
# #     age_expr = Expression(age_var, Variable(45, {}), Operator.LESS_THAN_OR_EQUAL)
# #     location_expr = Expression(location_var, Variable("NY", {}), Operator.NOT_EQUAL)

# #     and_expr1 = Expression(equals_expr, age_expr, Operator.AND)
# #     final_expr = Expression(and_expr1, location_expr, Operator.AND)

# #     print('Final result:', final_expr.evaluate())  # Output: True

# class ExpressionBuilder:
#     def build(self, expression):
#         tokens = expression.split()
#         stack = []

#         i = 0
#         while i < len(tokens):
#             token = tokens[i]
#             print(token)
#             if token in Operator:
#                 right = stack.pop()
#                 left = stack.pop()
#                 operator = token
#                 print(left, right, operator)
#                 stack.append(Expression(left, right, operator))
#             else:
#                 if token.isdigit():
#                     stack.append(Literal(int(token)))
#                 elif token.startswith('"') and token.endswith('"'):
#                     stack.append(Literal(token.strip('"')))
#                 else:
#                     stack.append(Variable(token))
#             i += 1

#         # The final expression is the root of our composite tree
#         return stack.pop()

# # Example usage
# variables = {
#     "name": "Bob",
#     "age": 36,
#     "location": "Boston"
# }

# expression = 'name == "Bob" && age <= 45 && location != "NY"'

# expression_builder = ExpressionBuilder()
# root_expression = expression_builder.build(expression)
# result = root_expression.evaluate(variables)

# print(f"Output: {result}")  # Output: True

import re
from abc import ABC, abstractmethod

# ExpressionComponent: The base class for all expression components
class ExpressionComponent(ABC):
    @abstractmethod
    def evaluate(self, variables):
        pass

# Leaf classes for variables and literals
class Variable(ExpressionComponent):
    def __init__(self, name):
        self.name = name

    def evaluate(self, variables):
        return variables[self.name]

class Literal(ExpressionComponent):
    def __init__(self, value):
        self.value = value

    def evaluate(self, variables):
        return self.value

# Composite class for binary expressions
class BinaryExpression(ExpressionComponent):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, variables):
        left_value = self.left.evaluate(variables)
        right_value = self.right.evaluate(variables)
        return self.operator.evaluate(left_value, right_value)

# Operator interface and concrete operators
class Operator(ABC):
    @abstractmethod
    def evaluate(self, left, right):
        pass

class EqualsOperator(Operator):
    def evaluate(self, left, right):
        return left == right

class NotEqualsOperator(Operator):
    def evaluate(self, left, right):
        return left != right

class LessThanOrEqualsOperator(Operator):
    def evaluate(self, left, right):
        return left <= right

class GreaterThanOrEqualsOperator(Operator):
    def evaluate(self, left, right):
        return left >= right

class AndOperator(Operator):
    def evaluate(self, left, right):
        return left and right

class OrOperator(Operator):
    def evaluate(self, left, right):
        return left or right

# Factory to create operator instances
class OperatorFactory:
    def __init__(self):
        self.operators = {
            "==": EqualsOperator(),
            "!=": NotEqualsOperator(),
            "<=": LessThanOrEqualsOperator(),
            ">=": GreaterThanOrEqualsOperator(),
            "&&": AndOperator(),
            "||": OrOperator()
        }

    def get_operator(self, symbol):
        return self.operators.get(symbol)

# Expression builder with improved tokenization
class ExpressionBuilder:
    def __init__(self, operator_factory):
        self.operator_factory = operator_factory

    def tokenize(self, expression):
        # Tokenizes based on operators, strings, variables, and numbers
        token_pattern = re.compile(r'(\w+|"[^"]*"|\d+|&&|\|\||==|!=|<=|>=|<|>|[()])')
        return token_pattern.findall(expression)

    def build(self, expression):
        tokens = self.tokenize(expression)
        stack = []

        for token in tokens:
            if token in self.operator_factory.operators:
                right = stack.pop()
                left = stack.pop()
                operator = self.operator_factory.get_operator(token)
                stack.append(BinaryExpression(left, operator, right))
            else:
                if token.isdigit():
                    stack.append(Literal(int(token)))
                elif token.startswith('"') and token.endswith('"'):
                    stack.append(Literal(token.strip('"')))
                else:
                    stack.append(Variable(token))

        # The final expression is the root of our composite tree
        return stack.pop()

# Example usage
variables = {
    "name": "Bob",
    "age": 36,
    "location": "Boston"
}

expression = 'name == "Bob" && age <= 45 && location != "NY"'

operator_factory = OperatorFactory()
expression_builder = ExpressionBuilder(operator_factory)
root_expression = expression_builder.build(expression)
result = root_expression.evaluate(variables)

print(f"Output: {result}")  # Output: True
