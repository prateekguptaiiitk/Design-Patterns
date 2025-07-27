// Enum for Coins
const Coin = Object.freeze({
  PENNY: 1,
  NICKEL: 5,
  DIME: 10,
  QUARTER: 25,
});

// Enum for Item Types
const ItemType = Object.freeze({
  COKE: 'COKE',
  PEPSI: 'PEPSI',
  JUICE: 'JUICE',
  SODA: 'SODA',
});

// Abstract State class
class State {
  clickOnInsertCoinButton(vm) { throw new Error('Not implemented'); }
  clickOnStartProductSelectionButton(vm) { throw new Error('Not implemented'); }
  insertCoin(vm, coin) { throw new Error('Not implemented'); }
  chooseProduct(vm, codeNumber) { throw new Error('Not implemented'); }
  getChange(returnChangeMoney) { throw new Error('Not implemented'); }
  dispenseProduct(vm, codeNumber) { throw new Error('Not implemented'); }
  refundFullMoney(vm) { throw new Error('Not implemented'); }
  updateInventory(vm, item, codeNumber) { throw new Error('Not implemented'); }
}

class IdleState extends State {
  constructor() {
    super();
    console.log('Currently Vending machine is in IdleState');
  }

  clickOnInsertCoinButton(vm) {
    vm.setVendingMachineState(new HasMoneyState());
  }

  clickOnStartProductSelectionButton() {
    throw new Error('First you need to click on insert coin button');
  }

  insertCoin() { throw new Error('You cannot insert coin in idle state'); }
  chooseProduct() { throw new Error('You cannot choose product in idle state'); }
  getChange() { throw new Error('You cannot get change in idle state'); }
  dispenseProduct() { throw new Error('Product cannot be dispensed in idle state'); }
  refundFullMoney() { throw new Error('You cannot get refunded in idle state'); }

  updateInventory(vm, item, codeNumber) {
    vm.getInventory().addItem(item, codeNumber);
  }
}

class HasMoneyState extends State {
  constructor() {
    super();
    console.log('Currently Vending machine is in HasMoneyState');
  }

  clickOnInsertCoinButton() {}

  clickOnStartProductSelectionButton(vm) {
    vm.setVendingMachineState(new SelectionState());
  }

  insertCoin(vm, coin) {
    console.log('Accepted the coin');
    vm.getCoinList().push(coin);
  }

  chooseProduct() { throw new Error('Start product selection first'); }
  getChange() { throw new Error('You cannot get change in HasMoneyState'); }
  dispenseProduct() { throw new Error('Product cannot be dispensed in HasMoneyState'); }

  refundFullMoney(vm) {
    console.log('Returned full amount');
    vm.setVendingMachineState(new IdleState());
    return vm.getCoinList();
  }

  updateInventory() { throw new Error('You cannot update inventory in HasMoneyState'); }
}

class SelectionState extends State {
  constructor() {
    super();
    console.log('Currently Vending machine is in SelectionState');
  }

  clickOnInsertCoinButton() { throw new Error('Not allowed in SelectionState'); }
  clickOnStartProductSelectionButton() {}
  insertCoin() { throw new Error('Cannot insert coin in selection state'); }

  chooseProduct(vm, codeNumber) {
    const item = vm.getInventory().getItem(codeNumber);
    const paid = vm.getCoinList().reduce((sum, c) => sum + c, 0);
    if (paid < item.getPrice()) {
      console.log(`Insufficient amount. Needed: ${item.getPrice()}, Paid: ${paid}`);
      this.refundFullMoney(vm);
      throw new Error('Insufficient amount');
    }
    if (paid > item.getPrice()) this.getChange(paid - item.getPrice());
    vm.setVendingMachineState(new DispenseState(vm, codeNumber));
  }

  getChange(returnChangeMoney) {
    console.log(`Returned change: ${returnChangeMoney}`);
    return returnChangeMoney;
  }

  dispenseProduct() { throw new Error('Not allowed in SelectionState'); }

  refundFullMoney(vm) {
    console.log('Returned full amount');
    vm.setVendingMachineState(new IdleState());
    return vm.getCoinList();
  }

  updateInventory() { throw new Error('Not allowed in SelectionState'); }
}

class DispenseState extends State {
  constructor(vm, codeNumber) {
    super();
    console.log('Currently Vending machine is in DispenseState');
    this.dispenseProduct(vm, codeNumber);
  }

  clickOnInsertCoinButton() { throw new Error('Not allowed in DispenseState'); }
  clickOnStartProductSelectionButton() { throw new Error('Not allowed in DispenseState'); }
  insertCoin() { throw new Error('Not allowed in DispenseState'); }
  chooseProduct() { throw new Error('Not allowed in DispenseState'); }
  getChange() { throw new Error('Not allowed in DispenseState'); }

  dispenseProduct(vm, codeNumber) {
    console.log('Product dispensed');
    const item = vm.getInventory().getItem(codeNumber);
    vm.getInventory().updateSoldOutItem(codeNumber);
    vm.setVendingMachineState(new IdleState());
    return item;
  }

  refundFullMoney() { throw new Error('Not allowed in DispenseState'); }
  updateInventory() { throw new Error('Not allowed in DispenseState'); }
}

class Item {
  constructor(type, price) {
    this.type = type;
    this.price = price;
  }
  getType() { return this.type; }
  getPrice() { return this.price; }
}

class ItemShelf {
  constructor() {
    this.code = 0;
    this.item = null;
    this.soldOut = true;
  }
  setCode(code) { this.code = code; }
  getCode() { return this.code; }
  getItem() { return this.item; }
  setItem(item) { this.item = item; }
  isSoldOut() { return this.soldOut; }
  setSoldOut(flag) { this.soldOut = flag; }
}

class Inventory {
  constructor(itemCount) {
    this.inventory = Array(itemCount).fill().map(() => new ItemShelf());
    this.initialEmptyInventory();
  }

  initialEmptyInventory() {
    let code = 101;
    this.inventory.forEach(shelf => {
      shelf.setCode(code++);
      shelf.setSoldOut(true);
    });
  }

  addItem(item, codeNumber) {
    const shelf = this.inventory.find(s => s.getCode() === codeNumber);
    if (shelf && shelf.isSoldOut()) {
      shelf.setItem(item);
      shelf.setSoldOut(false);
    } else {
      throw new Error('Cannot add item. Slot occupied or not found.');
    }
  }

  getItem(codeNumber) {
    const shelf = this.inventory.find(s => s.getCode() === codeNumber);
    if (!shelf || shelf.isSoldOut()) throw new Error('Item sold out or invalid code');
    return shelf.getItem();
  }

  updateSoldOutItem(codeNumber) {
    const shelf = this.inventory.find(s => s.getCode() === codeNumber);
    if (shelf) shelf.setSoldOut(true);
  }

  getInventory() { return this.inventory; }
}

class VendingMachine {
  constructor() {
    this.vendingMachineState = new IdleState();
    this.inventory = new Inventory(10);
    this.coinList = [];
  }

  getVendingMachineState() { return this.vendingMachineState; }
  setVendingMachineState(state) { this.vendingMachineState = state; }
  getInventory() { return this.inventory; }
  getCoinList() { return this.coinList; }
}

class Main {
  static run() {
    const vm = new VendingMachine();
    try {
      console.log('|\nFilling up inventory\n|');
      this.fillInventory(vm);
      this.displayInventory(vm);

      console.log('|\nClicking InsertCoinButton\n|');
      vm.getVendingMachineState().clickOnInsertCoinButton(vm);
      vm.getVendingMachineState().insertCoin(vm, Coin.NICKEL);
      vm.getVendingMachineState().insertCoin(vm, Coin.QUARTER);

      console.log('|\nClicking StartProductSelection\n|');
      vm.getVendingMachineState().clickOnStartProductSelectionButton(vm);
      vm.getVendingMachineState().chooseProduct(vm, 102);

      this.displayInventory(vm);
    } catch (e) {
      console.error('Exception:', e.message);
      this.displayInventory(vm);
    }
  }

  static fillInventory(vm) {
    const slots = vm.getInventory().getInventory();
    slots.forEach((shelf, i) => {
      let item;
      if (i < 3) item = new Item(ItemType.COKE, 12);
      else if (i < 5) item = new Item(ItemType.PEPSI, 9);
      else if (i < 7) item = new Item(ItemType.JUICE, 13);
      else item = new Item(ItemType.SODA, 7);
      shelf.setItem(item);
      shelf.setSoldOut(false);
    });
  }

  static displayInventory(vm) {
    vm.getInventory().getInventory().forEach(shelf => {
      console.log(
        `Code: ${shelf.getCode()} | Item: ${shelf.getItem().getType()} | Price: ${shelf.getItem().getPrice()} | Available: ${!shelf.isSoldOut()}`
      );
    });
  }
}

Main.run();