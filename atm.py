from abc import ABC, abstractmethod

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
        print('Card is inserted')
        atm.setCurrentATMState(HasCardState())
    
    def authenticatePin(self, atm, card, pin):
        isCorrectPinEntered = card.isCorrectPINEntered(pin)

        if isCorrectPinEntered:
            atm.setCurrentATMState(SelectOperationState())
        else:
            print('invalid pin number')
            exit(atm)
    
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
        print('Card is inserted')
        atm.setCurrentATMState(HasCardState())

    def authenticatePin(self, atm, card, pin):
        print("OOPS!! Something went wrong")
    
    def selectOperation(self, atm, card, txnType):
        if txnType == 'CASH_WITHDRAWAL':
            atm.setCurrentATMState(CashWithdrawalState())
        elif txnType == 'BALANCE_CHECK':
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
        print('Please select the operaton')
        TransactionType().showAllTransactionTypes()

class CashWithdrawalState(ATMState):
    def __init__(self):
        print('Please enter the withdrawal amount')
    
    def insertCard(self, atm, card):
        print('Card is inserted')
        atm.setCurrentATMState(HasCardState())

    def authenticatePin(self, atm, card, pin):
        print("OOPS!! Something went wrong")

    def selectOperation(self, atm, card, txnType):
        print("OOPS!! Something went wrong")
    
    def cashWithdrawal(self, atm, card, withdrawAmount):
        if atm.getAtmBalance() < withdrawAmount:
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
        print('Card is inserted')
        atm.setCurrentATMState(HasCardState())

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
    nextCashWithdrawalProcessor = None
    
    def __init__(self, cashWithdrawalProcessor):
        self.nextCashWithdrawalProcessor = cashWithdrawalProcessor

    def withdraw(self, atm, remainingAmount):
        if self.nextCashWithdrawalProcessor:
            self.nextCashWithdrawalProcessor.withdraw(atm, remainingAmount)

class TwoThousandWithdrawProcessor(CashWithdrawProcessor):
    
    def __init__(self, nextCashWithdrawalProcessor):
        super().__init__(nextCashWithdrawalProcessor)

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
    
    def __init__(self, nextCashWithdrawalProcessor):
        super().__init__(nextCashWithdrawalProcessor)

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
    
    def __init__(self, nextCashWithdrawalProcessor):
        super().__init__(nextCashWithdrawalProcessor)

    def withdraw(self, atm, remainingAmount):
        required = remainingAmount // 100
        balance = remainingAmount % 100

        if required <= atm.getNoOfOneHundredNotes():
            atm.deductOneHundredNotes(required)
        else:
            atm.deductOneHundredNotes(atm.getNoOfOneHundredNotes())
            balance += (required - atm.getNoOfOneHundredNotes()) * 2000
        
        if balance != 0:
            super().withdraw(atm, balance)