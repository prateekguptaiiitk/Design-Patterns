from abc import ABC, abstractmethod
from enum import Enum

class ATMState(ABC):
    @abstractmethod
    def insertCard(self, atm, card):
        print("OOPS!! Something went wrong")

    @abstractmethod
    def authenticatePin(self, atm, card, pin):
        print("OOPS!! Something went wrong")

    @abstractmethod
    def selectOperation(self, atm, card, txnType):
        print("OOPS!! Something went wrong")

    @abstractmethod
    def cashWithdrawal(self, atm, card, withdrawAmount):
        print("OOPS!! Something went wrong")

    @abstractmethod
    def displayBalance(self, atm, card):
        print("OOPS!! Something went wrong")

    @abstractmethod
    def returnCard(self):
        print("OOPS!! Something went wrong")

    @abstractmethod
    def exit(self, atm):
        print("OOPS!! Something went wrong")


class IdleState(ATMState):
    def insertCard(self, atm, card):
        print('Card is inserted')
        atm.setCurrentATMState(HasCardState())

    def authenticatePin(self, atm, card, pin):
        print("OOPS!! Something went wrong")

    def selectOperation(self, atm, card, txnType):
        print("OOPS!! Something went wrong")

    def cashWithdrawal(self, atm, card, withdrawAmount):
        print("OOPS!! Something went wrong")

    def displayBalance(self, atm, card):
        print("OOPS!! Something went wrong")

    def returnCard(self):
        print("OOPS!! Something went wrong")

    def exit(self, atm):
        print("OOPS!! Something went wrong")


class HasCardState(ATMState):
    def __init__(self):
        print('enter your card pin number')

    def insertCard(self, atm, card):
        print("Card already inserted")
    
    def authenticatePin(self, atm, card, pin):
        isCorrectPinEntered = card.isCorrectPINEntered(pin)

        if isCorrectPinEntered:
            atm.setCurrentATMState(SelectOperationState())
        else:
            print('invalid pin number')
            self.exit(atm)
    
    def selectOperation(self, atm, card, txnType):
        print("OOPS!! Something went wrong")
    
    def cashWithdrawal(self, atm, card, withdrawAmount):
        print("OOPS!! Something went wrong")
    
    def displayBalance(self, atm, card):
        print("OOPS!! Something went wrong")

    def exit(self, atm):
        self.returnCard()
        atm.setCurrentATMState(IdleState())
        print('exit happens')
    
    def returnCard(self):
        print('please collect your card')


class SelectOperationState(ATMState):
    def __init__(self):
        self.showOperations()
    
    def insertCard(self, atm, card):
        print("Card already inserted")

    def authenticatePin(self, atm, card, pin):
        print("OOPS!! Something went wrong")
    
    def selectOperation(self, atm, card, txnType):
        if txnType == TransactionType.CASH_WITHDRAWAL:
            atm.setCurrentATMState(CashWithdrawalState())
        elif txnType == TransactionType.BALANCE_CHECK:
            atm.setCurrentATMState(CheckBalanceState())
        else:
            print('Invalid Option')
            self.exit(atm)

    def cashWithdrawal(self, atm, card, withdrawAmount):
        print("OOPS!! Something went wrong")
    
    def displayBalance(self, atm, card):
        print("OOPS!! Something went wrong")

    def exit(self, atm):
        self.returnCard()
        atm.setCurrentATMState(IdleState())
        print('exit happens')
    
    def returnCard(self):
        print('please collect your card')

    def showOperations(self):
        print('Please select the operation')
        TransactionType.showAllTransactionTypes()

class CashWithdrawalState(ATMState):
    def __init__(self):
        print('Please enter the withdrawal amount')
    
    def insertCard(self, atm, card):
        print("Card already inserted")

    def authenticatePin(self, atm, card, pin):
        print("OOPS!! Something went wrong")

    def selectOperation(self, atm, card, txnType):
        print("OOPS!! Something went wrong")
    
    def cashWithdrawal(self, atm, card, withdrawAmount):
        if atm.getATMBalance() < withdrawAmount:
            print('Insufficient fund in the ATM Machine')
            self.exit(atm)
        elif card.getBankBalance() < withdrawAmount:
            print('Insufficient fund in your bank account')
        else:
            card.deductBankBalance(withdrawAmount)
            atm.deductATMBalance(withdrawAmount)

            # using chain of responsibility for this logic, how many Rs. 2k notes, how many Rs 500 notes, etc has to be withdrawed
            withdrawProcessor = TwoThousandWithdrawProcessor(FiveHundredWithdrawProcessor(OneHundredWithdrawProcessor(None)))
            withdrawProcessor.withdraw(atm, withdrawAmount)
            self.exit(atm)
    
    def displayBalance(self, atm, card):
        print("OOPS!! Something went wrong")

    def exit(self, atm):
        self.returnCard()
        atm.setCurrentATMState(IdleState())
        print('exit happens')
    
    def returnCard(self):
        print('please collect your card')


class CheckBalanceState(ATMState):
    def insertCard(self, atm, card):
        print("Card already inserted")

    def authenticatePin(self, atm, card, pin):
        print("OOPS!! Something went wrong")

    def selectOperation(self, atm, card, txnType):
        print("OOPS!! Something went wrong")

    def cashWithdrawal(self, atm, card, withdrawAmount):
        print("OOPS!! Something went wrong")

    def displayBalance(self, atm, card):
        print('Your balance is: ', card.getBankBalance())
        self.exit(atm)
    
    def exit(self, atm):
        self.returnCard()
        atm.setCurrentATMState(IdleState())
        print('exit happens')
    
    def returnCard(self):
        print('please collect your card')


class CashWithdrawProcessor(ABC):
    def __init__(self, nextCashWithdrawalProcessor):
        self.nextCashWithdrawalProcessor = nextCashWithdrawalProcessor

    def withdraw(self, atm, remainingAmount):
        if self.nextCashWithdrawalProcessor:
            self.nextCashWithdrawalProcessor.withdraw(atm, remainingAmount)


class TwoThousandWithdrawProcessor(CashWithdrawProcessor):
    def withdraw(self, atm, remainingAmount):
        required = remainingAmount // 2000
        balance = remainingAmount % 2000

        if required <= atm.getNoOfTwoThousandNotes():
            atm.deductTwoThousandNotes(required)
        else:
            atm.deductTwoThousandNotes(atm.getNoOfTwoThousandNotes())
            balance += (required - atm.getNoOfTwoThousandNotes()) * 2000
        
        if balance != 0:
            super().withdraw(atm, balance)


class FiveHundredWithdrawProcessor(CashWithdrawProcessor):
    def withdraw(self, atm, remainingAmount):
        required = remainingAmount // 500
        balance = remainingAmount % 500

        if required <= atm.getNoOfFiveHundredNotes():
            atm.deductFiveHundredNotes(required)
        else:
            atm.deductFiveHundredNotes(atm.getNoOfFiveHundredNotes())
            balance += (required - atm.getNoOfFiveHundredNotes()) * 500
        
        if balance != 0:
            super().withdraw(atm, balance)


class OneHundredWithdrawProcessor(CashWithdrawProcessor):
    def withdraw(self, atm, remainingAmount):
        required = remainingAmount // 100
        balance = remainingAmount % 100

        if required <= atm.getNoOfOneHundredNotes():
            atm.deductOneHundredNotes(required)
        else:
            atm.deductOneHundredNotes(atm.getNoOfOneHundredNotes())
            balance += (required - atm.getNoOfOneHundredNotes()) * 100
        
        if balance != 0:
            super().withdraw(atm, balance)

class ATM:
    def __init__(self):
        self.currentATMState = None
        self.atmBalance = 0
        self.noOfTwoThousandNotes = 0
        self.noOfFiveHundredNotes = 0
        self.noOfOneHundredNotes = 0

    def setCurrentATMState(self, currentATMState):
        self.currentATMState = currentATMState
    
    def getCurrentATMState(self):
        return self.currentATMState

    @staticmethod
    def getATMObject():
        atm = ATM()
        atm.setCurrentATMState(IdleState())
        return atm

    def getATMBalance(self):
        return self.atmBalance
    
    def setATMBalance(self, atmBalance, noOfTwoThousandNotes, noOfFiveHundredNotes, noOfOneHundredNotes):
        self.atmBalance = atmBalance
        self.noOfTwoThousandNotes = noOfTwoThousandNotes
        self.noOfFiveHundredNotes = noOfFiveHundredNotes
        self.noOfOneHundredNotes = noOfOneHundredNotes
    
    def getNoOfTwoThousandNotes(self):
        return self.noOfTwoThousandNotes
    
    def getNoOfFiveHundredNotes(self):
        return self.noOfFiveHundredNotes
    
    def getNoOfOneHundredNotes(self):
        return self.noOfOneHundredNotes
    
    def deductATMBalance(self, amount):
        self.atmBalance -= amount
    
    def deductTwoThousandNotes(self, number):
        self.noOfTwoThousandNotes -= number

    def deductFiveHundredNotes(self, number):
        self.noOfFiveHundredNotes -= number

    def deductOneHundredNotes(self, number):
        self.noOfOneHundredNotes -= number

    def printCurrentATMStatus(self):
        print("Balance: ", self.atmBalance)
        print("2kNotes: ", self.noOfTwoThousandNotes)
        print("500Notes: ", self.noOfFiveHundredNotes)
        print("100Notes: ", self.noOfOneHundredNotes)

class Card:
    def __init__(self):
        self.PIN_NUMBER = 112211
        self.bankAccount = None

    def isCorrectPINEntered(self, pin):
        return pin == self.PIN_NUMBER

    def getBankBalance(self):
        return self.bankAccount.balance

    def deductBankBalance(self, amount):
        self.bankAccount.withdrawalBalance(amount)

    def setBankAccount(self, bankAccount):
        self.bankAccount = bankAccount


class TransactionType(Enum):
    CASH_WITHDRAWAL = 'CASH_WITHDRAWAL'
    BALANCE_CHECK = 'BALANCE_CHECK'

    @staticmethod
    def showAllTransactionTypes():
        for txn_type in TransactionType:
            print(txn_type.name)


class User:
    def __init__(self):
        self.card = None

    def getCard(self):
        return self.card
    
    def setCard(self, card):
        self.card = card


class UserBankAccount:
    def __init__(self):
        self.balance = 0

    def withdrawalBalance(self, amount):
        self.balance -= amount


class ATMRoom:
    def __init__(self):
        self.atm = None
        self.user = None

    def main(self):
        self.initialize()
        self.atm.printCurrentATMStatus()
        self.atm.getCurrentATMState().insertCard(self.atm, self.user.card)
        self.atm.getCurrentATMState().authenticatePin(self.atm, self.user.card, 112211)
        self.atm.getCurrentATMState().selectOperation(self.atm, self.user.card, TransactionType.CASH_WITHDRAWAL)
        self.atm.getCurrentATMState().cashWithdrawal(self.atm, self.user.card, 2700)
        self.atm.printCurrentATMStatus()

    def initialize(self):
        # create ATM
        self.atm = ATM.getATMObject()
        self.atm.setATMBalance(3500, 1, 2, 5)

        # create User
        self.user = self.createUser()

    def createUser(self):
        user = User()
        user.setCard(self.createCard())
        return user

    def createCard(self):
        card = Card()
        card.setBankAccount(self.createBankAccount())
        return card

    def createBankAccount(self):
        bankAccount = UserBankAccount()
        bankAccount.balance = 3000
        return bankAccount


if __name__ == '__main__':
    atmRoom = ATMRoom()
    atmRoom.main()
