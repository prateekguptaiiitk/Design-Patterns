// Enums
const TransactionType = Object.freeze({
  CASH_WITHDRAWAL: 'CASH_WITHDRAWAL',
  BALANCE_CHECK: 'BALANCE_CHECK',
});

function showAllTransactionTypes() {
  Object.values(TransactionType).forEach((type) => console.log(type));
}

// ATM State Interface
class ATMState {
  insertCard(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  authenticatePin(atm, card, pin) {
    throw new Error('OOPS!! Something went wrong');
  }
  selectOperation(atm, card, txnType) {
    throw new Error('OOPS!! Something went wrong');
  }
  cashWithdrawal(atm, card, amount) {
    throw new Error('OOPS!! Something went wrong');
  }
  displayBalance(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  returnCard() {
    throw new Error('OOPS!! Something went wrong');
  }
  exit(atm) {
    throw new Error('OOPS!! Something went wrong');
  }
}

// IdleState
class IdleState extends ATMState {
  insertCard(atm, card) {
    console.log('Card is inserted');
    atm.setCurrentATMState(new HasCardState());
  }
  authenticatePin(atm, card, pin) {
    throw new Error('OOPS!! Something went wrong');
  }
  selectOperation(atm, card, txnType) {
    throw new Error('OOPS!! Something went wrong');
  }
  cashWithdrawal(atm, card, amount) {
    throw new Error('OOPS!! Something went wrong');
  }
  displayBalance(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  returnCard() {
    throw new Error('OOPS!! Something went wrong');
  }
  exit(atm) {
    throw new Error('OOPS!! Something went wrong');
  }
}

// HasCardState
class HasCardState extends ATMState {
  constructor() {
    super();
    console.log('Enter your card PIN number');
  }
  insertCard(atm, card) {
    console.log('Card already inserted');
  }
  authenticatePin(atm, card, pin) {
    if (card.isCorrectPINEntered(pin)) {
      atm.setCurrentATMState(new SelectOperationState());
    } else {
      console.log('Invalid PIN number');
      this.exit(atm);
    }
  }
  selectOperation(atm, card, txnType) {
    throw new Error('OOPS!! Something went wrong');
  }
  cashWithdrawal(atm, card, amount) {
    throw new Error('OOPS!! Something went wrong');
  }
  displayBalance(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  returnCard() {
    console.log('Please collect your card');
  }
  exit(atm) {
    this.returnCard();
    atm.setCurrentATMState(new IdleState());
    console.log('Exit happens');
  }
}

// SelectOperationState
class SelectOperationState extends ATMState {
  constructor() {
    super();
    console.log('Please select the operation');
    showAllTransactionTypes();
  }
  insertCard(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  authenticatePin(atm, card, pin) {
    throw new Error('OOPS!! Something went wrong');
  }
  selectOperation(atm, card, txnType) {
    if (txnType === TransactionType.CASH_WITHDRAWAL) {
      atm.setCurrentATMState(new CashWithdrawalState());
    } else if (txnType === TransactionType.BALANCE_CHECK) {
      atm.setCurrentATMState(new CheckBalanceState());
    } else {
      console.log('Invalid Option');
      this.exit(atm);
    }
  }
  cashWithdrawal(atm, card, amount) {
    throw new Error('OOPS!! Something went wrong');
  }
  displayBalance(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  returnCard() {
    console.log('Please collect your card');
  }
  exit(atm) {
    this.returnCard();
    atm.setCurrentATMState(new IdleState());
    console.log('Exit happens');
  }
}

// CashWithdrawalState
class CashWithdrawalState extends ATMState {
  constructor() {
    super();
    console.log('Please enter the withdrawal amount');
  }
  insertCard(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  authenticatePin(atm, card, pin) {
    throw new Error('OOPS!! Something went wrong');
  }
  selectOperation(atm, card, txnType) {
    throw new Error('OOPS!! Something went wrong');
  }
  cashWithdrawal(atm, card, amount) {
    if (atm.getATMBalance() < amount) {
      console.log('Insufficient fund in the ATM Machine');
      this.exit(atm);
    } else if (card.getBankBalance() < amount) {
      console.log('Insufficient fund in your bank account');
    } else {
      card.deductBankBalance(amount);
      atm.deductATMBalance(amount);
      const processor = new TwoThousandWithdrawProcessor(new FiveHundredWithdrawProcessor(new OneHundredWithdrawProcessor(null)));
      processor.withdraw(atm, amount);
      this.exit(atm);
    }
  }
  displayBalance(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  returnCard() {
    console.log('Please collect your card');
  }
  exit(atm) {
    this.returnCard();
    atm.setCurrentATMState(new IdleState());
    console.log('Exit happens');
  }
}

// CheckBalanceState
class CheckBalanceState extends ATMState {
  insertCard(atm, card) {
    throw new Error('OOPS!! Something went wrong');
  }
  authenticatePin(atm, card, pin) {
    throw new Error('OOPS!! Something went wrong');
  }
  selectOperation(atm, card, txnType) {
    throw new Error('OOPS!! Something went wrong');
  }
  cashWithdrawal(atm, card, amount) {
    throw new Error('OOPS!! Something went wrong');
  }
  displayBalance(atm, card) {
    console.log('Your balance is: ', card.getBankBalance());
    this.exit(atm);
  }  
  returnCard() {
    console.log('Please collect your card');
  }
  exit(atm) {
    this.returnCard();
    atm.setCurrentATMState(new IdleState());
    console.log('Exit happens');
  }
}

// Chain of Responsibility Processors
class CashWithdrawProcessor {
  constructor(next) {
    this.next = next;
  }
  withdraw(atm, amount) {
    if (this.next) this.next.withdraw(atm, amount);
  }
}

class TwoThousandWithdrawProcessor extends CashWithdrawProcessor {
  withdraw(atm, amount) {
    let required = Math.floor(amount / 2000);
    let balance = amount % 2000;
    if (required <= atm.getNoOfTwoThousandNotes()) {
      atm.deductTwoThousandNotes(required);
    } else {
      let available = atm.getNoOfTwoThousandNotes();
      atm.deductTwoThousandNotes(available);
      balance += (required - available) * 2000;
    }
    super.withdraw(atm, balance);
  }
}

class FiveHundredWithdrawProcessor extends CashWithdrawProcessor {
  withdraw(atm, amount) {
    let required = Math.floor(amount / 500);
    let balance = amount % 500;
    if (required <= atm.getNoOfFiveHundredNotes()) {
      atm.deductFiveHundredNotes(required);
    } else {
      let available = atm.getNoOfFiveHundredNotes();
      atm.deductFiveHundredNotes(available);
      balance += (required - available) * 500;
    }
    super.withdraw(atm, balance);
  }
}

class OneHundredWithdrawProcessor extends CashWithdrawProcessor {
  withdraw(atm, amount) {
    let required = Math.floor(amount / 100);
    let balance = amount % 100;
    if (required <= atm.getNoOfOneHundredNotes()) {
      atm.deductOneHundredNotes(required);
    } else {
      let available = atm.getNoOfOneHundredNotes();
      atm.deductOneHundredNotes(available);
      balance += (required - available) * 100;
    }
    super.withdraw(atm, balance);
  }
}

// ATM
class ATM {
  constructor() {
    this.currentATMState = null
    this.atmBalance = 0;
    this.noOfTwoThousandNotes = 0;
    this.noOfFiveHundredNotes = 0;
    this.noOfOneHundredNotes = 0;
  }
  setCurrentATMState(state) {
    this.currentATMState = state;
  }
  getCurrentATMState() {
    return this.currentATMState;
  }
  static getATMObject() {
    const atm = new ATM();
    atm.setCurrentATMState(new IdleState())
    return atm
  }
  setATMBalance(balance, t2k, t500, t100) {
    this.atmBalance = balance;
    this.noOfTwoThousandNotes = t2k;
    this.noOfFiveHundredNotes = t500;
    this.noOfOneHundredNotes = t100;
  }
  getATMBalance() {
    return this.atmBalance;
  }
  deductATMBalance(amount) {
    this.atmBalance -= amount;
  }
  getNoOfTwoThousandNotes() {
    return this.noOfTwoThousandNotes;
  }
  getNoOfFiveHundredNotes() {
    return this.noOfFiveHundredNotes;
  }
  getNoOfOneHundredNotes() {
    return this.noOfOneHundredNotes;
  }
  deductTwoThousandNotes(num) {
    this.noOfTwoThousandNotes -= num;
  }
  deductFiveHundredNotes(num) {
    this.noOfFiveHundredNotes -= num;
  }
  deductOneHundredNotes(num) {
    this.noOfOneHundredNotes -= num;
  }
  printCurrentATMStatus() {
    console.log('Balance:', this.atmBalance);
    console.log('2kNotes:', this.noOfTwoThousandNotes);
    console.log('500Notes:', this.noOfFiveHundredNotes);
    console.log('100Notes:', this.noOfOneHundredNotes);
  }
}

// Card
class Card {
  constructor() {
    this.PIN_NUMBER = 112211;
    this.bankAccount = null;
  }
  isCorrectPINEntered(pin) {
    return pin === this.PIN_NUMBER;
  }
  getBankBalance() {
    return this.bankAccount.balance;
  }
  deductBankBalance(amount) {
    this.bankAccount.withdrawalBalance(amount);
  }
  setBankAccount(bankAccount) {
    this.bankAccount = bankAccount;
  }
}

// User
class User {
  constructor() {
    this.card = null;
  }
  getCard() {
    return this.card;
  }
  setCard(card) {
    this.card = card;
  }
}

// UserBankAccount
class UserBankAccount {
  constructor() {
    this.balance = 0;
  }
  withdrawalBalance(amount) {
    this.balance -= amount;
  }
}

// ATMRoom
class ATMRoom {
  main() {
    this.initialize();
    this.atm.printCurrentATMStatus();
    this.atm.getCurrentATMState().insertCard(this.atm, this.user.getCard());
    this.atm.getCurrentATMState().authenticatePin(this.atm, this.user.getCard(), 112211);
    this.atm.getCurrentATMState().selectOperation(this.atm, this.user.getCard(), TransactionType.CASH_WITHDRAWAL);
    this.atm.getCurrentATMState().cashWithdrawal(this.atm, this.user.getCard(), 2700);
    this.atm.printCurrentATMStatus();
  }
  initialize() {
    this.atm = ATM.getATMObject();
    this.atm.setATMBalance(3500, 1, 2, 5);
    this.user = this.createUser();
  }
  createUser() {
    const user = new User();
    user.setCard(this.createCard());
    return user;
  }
  createCard() {
    const card = new Card();
    card.setBankAccount(this.createBankAccount());
    return card;
  }
  createBankAccount() {
    const account = new UserBankAccount();
    account.balance = 3000;
    return account;
  }
}

// Run the system
const atmRoom = new ATMRoom();
atmRoom.main();