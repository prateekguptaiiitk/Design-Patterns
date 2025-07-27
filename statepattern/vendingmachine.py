from abc import ABC, abstractmethod
from enum import Enum

# Abstract State class
class State(ABC):
    @abstractmethod
    def clickOnInsertCoinButton(self, vendingMachine):
        pass

    @abstractmethod
    def clickOnStartProductSelectionButton(self, vendingMachine):
        pass

    @abstractmethod
    def insertCoin(self, vendingMachine, coin):
        pass

    @abstractmethod
    def chooseProduct(self, vendingMachine, codeNumber):
        pass

    @abstractmethod
    def getChange(self, returnChangeMoney):
        pass

    @abstractmethod
    def dispenseProduct(self, vendingMachine, codeNumber):
        pass

    @abstractmethod
    def refundFullMoney(self, vendingMachine):
        pass

    @abstractmethod
    def updateInventory(self, vendingMachine, item, codeNumber):
        pass

# Idle State class
class IdleState(State):
    def __init__(self):
        print("Currently Vending machine is in IdleState")

    def clickOnInsertCoinButton(self, vendingMachine):
        vendingMachine.setVendingMachineState(HasMoneyState())

    def clickOnStartProductSelectionButton(self, vendingMachine):
        raise Exception("First you need to click on insert coin button")

    def insertCoin(self, vendingMachine, coin):
        raise Exception("You cannot insert coin in idle state")

    def chooseProduct(self, vendingMachine, codeNumber):
        raise Exception("You cannot choose product in idle state")

    def getChange(self, returnChangeMoney):
        raise Exception("You cannot get change in idle state")

    def dispenseProduct(self, vendingMachine, codeNumber):
        raise Exception("Product cannot be dispensed in idle state")

    def refundFullMoney(self, vendingMachine):
        raise Exception("You cannot get refunded in idle state")

    def updateInventory(self, vendingMachine, item, codeNumber):
        vendingMachine.getInventory().addItem(item, codeNumber)

# HasMoney State class
class HasMoneyState(State):
    def __init__(self):
        print("Currently Vending machine is in HasMoneyState")

    def clickOnInsertCoinButton(self, vendingMachine):
        return

    def clickOnStartProductSelectionButton(self, vendingMachine):
        vendingMachine.setVendingMachineState(SelectionState())

    def insertCoin(self, vendingMachine, coin):
        print("Accepted the coin")
        vendingMachine.getCoinList().append(coin)

    def chooseProduct(self, vendingMachine, codeNumber):
        raise Exception("You need to click on start product selection button first")

    def getChange(self, returnChangeMoney):
        raise Exception("You cannot get change in hasMoney state")

    def dispenseProduct(self, vendingMachine, codeNumber):
        raise Exception("Product cannot be dispensed in hasMoney state")

    def refundFullMoney(self, vendingMachine):
        print("Returned the full amount back in the Coin Dispense Tray")
        vendingMachine.setVendingMachineState(IdleState())
        return vendingMachine.getCoinList()

    def updateInventory(self, vendingMachine, item, codeNumber):
        raise Exception("You cannot update inventory in hasMoney state")

# Selection State class
class SelectionState(State):
    def __init__(self):
        print("Currently Vending machine is in SelectionState")

    def clickOnInsertCoinButton(self, vendingMachine):
        raise Exception("You cannot click on insert coin button in Selection state")

    def clickOnStartProductSelectionButton(self, vendingMachine):
        return

    def insertCoin(self, vendingMachine, coin):
        raise Exception("You cannot insert coin in selection state")

    def chooseProduct(self, vendingMachine, codeNumber):
        item = vendingMachine.getInventory().getItem(codeNumber)
        paidByUser = sum(coin.value for coin in vendingMachine.getCoinList())
        
        if paidByUser < item.getPrice():
            print("Insufficient Amount, Product you selected is for price: ", item.getPrice(), " and you paid: ", paidByUser)
            self.refundFullMoney(vendingMachine)
            raise Exception("Insufficient amount")
        elif paidByUser >= item.getPrice():
            if paidByUser > item.getPrice():
                self.getChange(paidByUser - item.getPrice())
            vendingMachine.setVendingMachineState(DispenseState(vendingMachine, codeNumber))

    def getChange(self, returnChangeMoney):
        print("Returned the change in the Coin Dispense Tray: ", returnChangeMoney)
        return returnChangeMoney

    def dispenseProduct(self, vendingMachine, codeNumber):
        raise Exception("Product cannot be dispensed in Selection state")

    def refundFullMoney(self, vendingMachine):
        print("Returned the full amount back in the Coin Dispense Tray")
        vendingMachine.setVendingMachineState(IdleState())
        return vendingMachine.getCoinList()

    def updateInventory(self, vendingMachine, item, codeNumber):
        raise Exception("Inventory cannot be updated in Selection state")

# Dispense State class
class DispenseState(State):
    def __init__(self, vendingMachine, codeNumber):
        print("Currently Vending machine is in DispenseState")
        self.dispenseProduct(vendingMachine, codeNumber)

    def clickOnInsertCoinButton(self, vendingMachine):
        raise Exception("Insert coin button cannot be clicked in Dispense state")

    def clickOnStartProductSelectionButton(self, vendingMachine):
        raise Exception("Product selection button cannot be clicked in Dispense state")

    def insertCoin(self, vendingMachine, coin):
        raise Exception("Coin cannot be inserted in Dispense state")

    def chooseProduct(self, vendingMachine, codeNumber):
        raise Exception("Product cannot be chosen in Dispense state")

    def getChange(self, returnChangeMoney):
        raise Exception("Change cannot be returned in Dispense state")

    def dispenseProduct(self, vendingMachine, codeNumber):
        print("Product has been dispensed")
        item = vendingMachine.getInventory().getItem(codeNumber)
        vendingMachine.getInventory().updateSoldOutItem(codeNumber)
        vendingMachine.setVendingMachineState(IdleState())
        return item

    def refundFullMoney(self, vendingMachine):
        raise Exception("Refund cannot happen in Dispense state")

    def updateInventory(self, vendingMachine, item, codeNumber):
        raise Exception("Inventory cannot be updated in Dispense state")

# Coin Enum class
class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25

# Inventory class
class Inventory:
    def __init__(self, itemCount):
        self.inventory = [None] * itemCount
        self.initialEmptyInventory()

    def getInventory(self):
        return self.inventory

    def setInventory(self, inventory):
        self.inventory = inventory

    def initialEmptyInventory(self):
        startCode = 101
        for i in range(len(self.inventory)):
            space = ItemShelf()
            space.setCode(startCode)
            space.setSoldOut(True)
            self.inventory[i] = space
            startCode += 1

    def addItem(self, item, codeNumber):
        for itemShelf in self.inventory:
            if itemShelf.code == codeNumber:
                if itemShelf.isSoldOut():
                    itemShelf.item = item
                    itemShelf.setSoldOut(False)
                else:
                    raise Exception("Already item is present, you cannot add item here")

    def getItem(self, codeNumber):
        for itemShelf in self.inventory:
            if itemShelf.code == codeNumber:
                if itemShelf.isSoldOut():
                    raise Exception("Item already sold out")
                else:
                    return itemShelf.item
        raise Exception("Invalid Code")

    def updateSoldOutItem(self, codeNumber):
        for itemShelf in self.inventory:
            if itemShelf.code == codeNumber:
                itemShelf.setSoldOut(True)

# Item class
class Item:
    def __init__(self):
        self.type = None
        self.price = 0

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

# ItemShelf class
class ItemShelf:
    def __init__(self):
        self.code = 0
        self.item = None
        self.soldOut = False

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getItem(self):
        return self.item

    def setItem(self, item):
        self.item = item

    def isSoldOut(self):
        return self.soldOut

    def setSoldOut(self, soldOut):
        self.soldOut = soldOut

# ItemType Enum class
class ItemType(Enum):
    COKE = 'COKE'
    PEPSI = 'PEPSI'
    JUICE = 'JUICE'
    SODA = 'SODA'

# VendingMachine class
class VendingMachine:
    def __init__(self):
        self.vendingMachineState = IdleState()
        self.inventory = Inventory(10)
        self.coinList = []

    def getVendingMachineState(self):
        return self.vendingMachineState

    def setVendingMachineState(self, vendingMachineState):
        self.vendingMachineState = vendingMachineState

    def getInventory(self):
        return self.inventory

    def setInventory(self, inventory):
        self.inventory = inventory

    def getCoinList(self):
        return self.coinList

    def setCoinList(self, coinList):
        self.coinList = coinList

# Main class
class Main:
    def main(self):
        vendingMachine = VendingMachine()

        try:
            print("|")
            print("Filling up the inventory")
            print("|")

            self.fillUpInventory(vendingMachine)
            self.displayInventory(vendingMachine)

            print("|")
            print("Clicking on InsertCoinButton")
            print("|")

            vendingState = vendingMachine.getVendingMachineState()
            vendingState.clickOnInsertCoinButton(vendingMachine)

            vendingState = vendingMachine.getVendingMachineState()
            vendingState.insertCoin(vendingMachine, Coin.NICKEL)
            vendingState.insertCoin(vendingMachine, Coin.QUARTER)

            print("|")
            print("Clicking on ProductSelectionButton")
            print("|")
            vendingState.clickOnStartProductSelectionButton(vendingMachine)

            codeNumber = 102
            vendingState = vendingMachine.getVendingMachineState()
            vendingState.chooseProduct(vendingMachine, codeNumber)

            vendingState = vendingMachine.getVendingMachineState()

            self.displayInventory(vendingMachine)

        except Exception as e:
            print("Exception occurred: ", str(e))
            self.displayInventory(vendingMachine)

    def fillUpInventory(self, vendingMachine):
        slots = vendingMachine.getInventory().getInventory()
        for i in range(len(slots)):
            newItem = Item()
            if i >= 0 and i < 3:
                newItem.setType(ItemType.COKE)
                newItem.setPrice(12)
            elif i >= 3 and i < 5:
                newItem.setType(ItemType.PEPSI)
                newItem.setPrice(9)
            elif i >= 5 and i < 7:
                newItem.setType(ItemType.JUICE)
                newItem.setPrice(13)
            elif i >= 7 and i < 10:
                newItem.setType(ItemType.SODA)
                newItem.setPrice(7)

            slots[i].setItem(newItem)
            slots[i].setSoldOut(False)

    def displayInventory(self, vendingMachine):
        slots = vendingMachine.getInventory().getInventory()
        for i in range(len(slots)):
            print("CodeNumber: ", slots[i].getCode(),
                  " Item: ", slots[i].getItem().getType().name,
                  " Price: ", slots[i].getItem().getPrice(),
                  " isAvailable: ", not slots[i].isSoldOut())

if __name__ == "__main__":
    obj = Main()
    obj.main()
