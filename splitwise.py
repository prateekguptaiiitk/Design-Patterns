from abc import ABC, abstractmethod

class ExpenseSplit(ABC):
    @abstractmethod
    def validateSplitRequest(self, splitList, totalAmount):
        pass

class EqualExpenseSplit(ExpenseSplit):

    def validateSplitRequest(self, splitList, totalAmount):
        # validate total amount in splits of each user is equal and overall equals to totalAmount
        amountShouldBePresent = totalAmount // len(splitList)

        for split in splitList:
            if split.getAmountOwe() != amountShouldBePresent:
                raise Exception('')
            
class UnequalExpenseSplit(ExpenseSplit):
    def validateSplitRequest(self, splitList, totalAmount):
        return 

class PercentageExpenseSplit(ExpenseSplit):
    def validateSplitRequest(self, splitList, totalAmount):
        return 
    
class Split:
    user = None
    amountOwe = 0.0

    def __init__(self, user, amount):
        self.user = user
        self.amountOwe = amount

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user
    
    def getAmountOwe(self):
        return self.amountOwe
    
    def setAmountOwe(self, amount):
        self.amountOwe = amount

class Expense:
    expenseId = None
    description = None
    expenseAmount = 0.0
    paidByUser = None
    splitType = None
    splitDetails = None

    def __init__(self, expenseId, description, expenseAmount, paidByUser, splitType, splitDetails):
        self.expenseId = expenseId
        self.description = description
        self.expenseAmount = expenseAmount
        self.paidByUser = paidByUser
        self.splitType = splitType
        self.splitDetails = splitDetails

class ExpenseController:
    balanceSheetController = None

    def __init__(self):
        self.balanceSheetController = BalanceSheetController()

    def createExpense(self, expenseId, description, expenseAmount, paidByUser, splitType, splitDetails):
        expenseSplit = SplitFactory().getSplitObject(splitType)
        expenseSplit.validateSplitRequest(splitDetails, expenseAmount)
        expense = Expense(description, expenseAmount, paidByUser, splitType, splitDetails)

        self.balanceSheetController.updateUserExpenseBalanceSheet(paidByUser, splitDetails, expenseAmount)

        return expense

from enum import Enum
class ExpenseSplitType(Enum):
    EQUAL = 'EQUAL'
    UNEQUAL = 'UNEQUAL'
    PERCENTAGE = 'PERCENTAGE'

class SplitFactory:
    def getgetSplitObject(self, splitType):
        if splitType == 'EQUAL':
            return EqualExpenseSplit()
        elif splitType == 'UNEQUAL':
            return UnequalExpenseSplit()
        elif splitType == 'PERCENTAGE':
            return PercentageExpenseSplit()
        else:
            return None

class Group:
    groupId = None
    groupName = None
    groupMembers = None

    expenseList = None
    expenseController = None

    def __init__(self):
        self.groupMembers = []
        self.expenseList = []
        self.expenseController = ExpenseController()

    # add member to group
    def addMember(self, member):
        self.groupMembers.append(member)

    def getGroupId(self):
        return self.groupId
    
    def setGroupId(self, groupId):
        self.groupId = groupId

    def setGroupName(self, groupName):
        self.groupName = groupName
    
    def createExpense(self,  expenseId, description, expenseAmount, paidByUser, splitType, splitDetails):
        expense = Expense(description, expenseAmount, paidByUser, splitType, splitDetails)
        self.expenseList.append(expense)
        return expense