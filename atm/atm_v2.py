from abc import ABC, abstractmethod
import threading
from typing import Optional, Dict
from enum import Enum

# interface
class DispenseChain(ABC):
    @abstractmethod
    def set_next_chain(self, next_chain: 'DispenseChain'):
        pass
    
    @abstractmethod
    def dispense(self, amount: int):
        pass
    
    @abstractmethod
    def can_dispense(self, amount: int) -> bool:
        pass


# abstract class
class NoteDispenser(DispenseChain, ABC):
    def __init__(self, note_value: int, num_notes: int):
        self._note_value = note_value
        self._num_notes = num_notes
        self._next_chain: Optional[DispenseChain] = None
        self._lock = threading.Lock()
    
    def set_next_chain(self, next_chain: DispenseChain):
        self._next_chain = next_chain
    
    def dispense(self, amount: int):
        with self._lock:
            if amount >= self._note_value:
                num_to_dispense = min(amount // self._note_value, self._num_notes)
                remaining_amount = amount - (num_to_dispense * self._note_value)
                
                if num_to_dispense > 0:
                    print(f"Dispensing {num_to_dispense} x ${self._note_value} note(s)")
                    self._num_notes -= num_to_dispense
                
                if remaining_amount > 0 and self._next_chain is not None:
                    self._next_chain.dispense(remaining_amount)
            elif self._next_chain is not None:
                self._next_chain.dispense(amount)
    
    def can_dispense(self, amount: int) -> bool:
        with self._lock:
            if amount < 0:
                return False
            if amount == 0:
                return True
            
            num_to_use = min(amount // self._note_value, self._num_notes)
            remaining_amount = amount - (num_to_use * self._note_value)
            
            if remaining_amount == 0:
                return True
            if self._next_chain is not None:
                return self._next_chain.can_dispense(remaining_amount)
            return False
        
class NoteDispenser20(NoteDispenser):
    def __init__(self, num_notes: int):
        super().__init__(20, num_notes)

class NoteDispenser50(NoteDispenser):
    def __init__(self, num_notes: int):
        super().__init__(50, num_notes)

class NoteDispenser100(NoteDispenser):
    def __init__(self, num_notes: int):
        super().__init__(100, num_notes)


class Card:
    def __init__(self, card_number: str, pin: str):
        self._card_number = card_number
        self._pin = pin
    
    def get_card_number(self) -> str:
        return self._card_number
    
    def get_pin(self) -> str:
        return self._pin


class Account:
    def __init__(self, account_number: str, balance: float):
        self._account_number = account_number
        self._balance = balance
        self._cards: Dict[str, Card] = {}
        self._lock = threading.Lock()
    
    def get_account_number(self) -> str:
        return self._account_number
    
    def get_balance(self) -> float:
        return self._balance
    
    def get_cards(self) -> Dict[str, Card]:
        return self._cards
    
    def deposit(self, amount: float):
        with self._lock:
            self._balance += amount
    
    def withdraw(self, amount: float) -> bool:
        with self._lock:
            if self._balance >= amount:
                self._balance -= amount
                return True
            return False


class BankService:
    def __init__(self):
        self._accounts: Dict[str, Account] = {}
        self._cards: Dict[str, Card] = {}
        self._card_account_map: Dict[Card, Account] = {}
        
        # Create sample accounts and cards
        account1 = self.create_account("1234567890", 1000.0)
        card1 = self.create_card("1234-5678-9012-3456", "1234")
        self.link_card_to_account(card1, account1)
        
        account2 = self.create_account("9876543210", 500.0)
        card2 = self.create_card("9876-5432-1098-7654", "4321")
        self.link_card_to_account(card2, account2)
    
    def create_account(self, account_number: str, initial_balance: float) -> Account:
        account = Account(account_number, initial_balance)
        self._accounts[account_number] = account
        return account
    
    def create_card(self, card_number: str, pin: str) -> Card:
        card = Card(card_number, pin)
        self._cards[card_number] = card
        return card
    
    def authenticate(self, card: Card, pin: str) -> bool:
        return card.get_pin() == pin
    
    def authenticate_card(self, card_number: str) -> Optional[Card]:
        return self._cards.get(card_number)
    
    def get_balance(self, card: Card) -> float:
        return self._card_account_map[card].get_balance()
    
    def withdraw_money(self, card: Card, amount: float):
        self._card_account_map[card].withdraw(amount)
    
    def deposit_money(self, card: Card, amount: float):
        self._card_account_map[card].deposit(amount)
    
    def link_card_to_account(self, card: Card, account: Account):
        account.get_cards()[card.get_card_number()] = card
        self._card_account_map[card] = account



class CashDispenser:
    def __init__(self, chain: DispenseChain):
        self._chain = chain
        self._lock = threading.Lock()
    
    def dispense_cash(self, amount: int):
        with self._lock:
            self._chain.dispense(amount)
    
    def can_dispense_cash(self, amount: int) -> bool:
        with self._lock:
            if amount % 10 != 0:
                return False
            return self._chain.can_dispense(amount)



class OperationType(Enum):
    CHECK_BALANCE = "CHECK_BALANCE"
    WITHDRAW_CASH = "WITHDRAW_CASH"
    DEPOSIT_CASH = "DEPOSIT_CASH"


# interface
class ATMState(ABC):
    @abstractmethod
    def insert_card(self, atm: 'ATM', card_number: str):
        pass
    
    @abstractmethod
    def enter_pin(self, atm: 'ATM', pin: str):
        pass
    
    @abstractmethod
    def select_operation(self, atm: 'ATM', op: OperationType, *args):
        pass
    
    @abstractmethod
    def eject_card(self, atm: 'ATM'):
        pass

class IdleState(ATMState):
    def insert_card(self, atm: 'ATM', card_number: str):
        print("\nCard has been inserted.")
        card = atm.get_bank_service().authenticate_card(card_number)
        
        if card is None:
            self.eject_card(atm)
        else:
            atm.set_current_card(card)
            atm.change_state(HasCardState())
    
    def enter_pin(self, atm: 'ATM', pin: str):
        print("Error: Please insert a card first.")
    
    def select_operation(self, atm: 'ATM', op: OperationType, *args):
        print("Error: Please insert a card first.")
    
    def eject_card(self, atm: 'ATM'):
        print("Error: Card not found.")

class HasCardState(ATMState):
    def insert_card(self, atm: 'ATM', card_number: str):
        print("Error: A card is already inserted. Cannot insert another card.")
    
    def enter_pin(self, atm: 'ATM', pin: str):
        print("Authenticating PIN...")
        card = atm.get_current_card()
        is_authenticated = atm.get_bank_service().authenticate(card, pin)
        
        if is_authenticated:
            print("Authentication successful.")
            atm.change_state(AuthenticatedState())
        else:
            print("Authentication failed: Incorrect PIN.")
            self.eject_card(atm)
    
    def select_operation(self, atm: 'ATM', op: OperationType, *args):
        print("Error: Please enter your PIN first to select an operation.")
    
    def eject_card(self, atm: 'ATM'):
        print("Card has been ejected. Thank you for using our ATM.")
        atm.set_current_card(None)
        atm.change_state(IdleState())

class AuthenticatedState(ATMState):
    def insert_card(self, atm: 'ATM', card_number: str):
        print("Error: A card is already inserted and a session is active.")
    
    def enter_pin(self, atm: 'ATM', pin: str):
        print("Error: PIN has already been entered and authenticated.")
    
    def select_operation(self, atm: 'ATM', op: OperationType, *args):
        if op == OperationType.CHECK_BALANCE:
            atm.check_balance()
        elif op == OperationType.WITHDRAW_CASH:
            if len(args) == 0 or args[0] <= 0:
                print("Error: Invalid withdrawal amount specified.")
                return
            
            amount_to_withdraw = args[0]
            account_balance = atm.get_bank_service().get_balance(atm.get_current_card())
            
            if amount_to_withdraw > account_balance:
                print("Error: Insufficient balance.")
                return
            
            print(f"Processing withdrawal for ${amount_to_withdraw}")
            atm.withdraw_cash(amount_to_withdraw)
        elif op == OperationType.DEPOSIT_CASH:
            if len(args) == 0 or args[0] <= 0:
                print("Error: Invalid deposit amount specified.")
                return
            
            amount_to_deposit = args[0]
            print(f"Processing deposit for ${amount_to_deposit}")
            atm.deposit_cash(amount_to_deposit)
        else:
            print("Error: Invalid operation selected.")
            return
        
        # End the session after one transaction
        print("Transaction complete.")
        self.eject_card(atm)
    
    def eject_card(self, atm: 'ATM'):
        print("Ending session. Card has been ejected. Thank you for using our ATM.")
        atm.set_current_card(None)
        atm.change_state(IdleState())



class ATM:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._current_state = IdleState()
            self._bank_service = BankService()
            self._current_card: Optional[Card] = None
            self._transaction_counter = 0
            
            # Setup the dispenser chain
            c1 = NoteDispenser100(10)  # 10 x $100 notes
            c2 = NoteDispenser50(20)   # 20 x $50 notes
            c3 = NoteDispenser20(30)   # 30 x $20 notes
            c1.set_next_chain(c2)
            c2.set_next_chain(c3)
            self._cash_dispenser = CashDispenser(c1)
            self._initialized = True
    
    @classmethod
    def get_instance(cls):
        return cls()
    
    def change_state(self, new_state: ATMState):
        self._current_state = new_state
    
    def set_current_card(self, card: Optional[Card]):
        self._current_card = card
    
    def insert_card(self, card_number: str):
        self._current_state.insert_card(self, card_number)
    
    def enter_pin(self, pin: str):
        self._current_state.enter_pin(self, pin)
    
    def select_operation(self, op: OperationType, *args):
        self._current_state.select_operation(self, op, *args)
    
    def check_balance(self):
        balance = self._bank_service.get_balance(self._current_card)
        print(f"Your current account balance is: ${balance:.2f}")
    
    def withdraw_cash(self, amount: int):
        if not self._cash_dispenser.can_dispense_cash(amount):
            raise RuntimeError("Insufficient cash available in the ATM.")
        
        self._bank_service.withdraw_money(self._current_card, amount)
        
        try:
            self._cash_dispenser.dispense_cash(amount)
        except Exception as e:
            self._bank_service.deposit_money(self._current_card, amount)  # Deposit back if dispensing fails
            raise e
    
    def deposit_cash(self, amount: int):
        self._bank_service.deposit_money(self._current_card, amount)
    
    def get_current_card(self) -> Optional[Card]:
        return self._current_card
    
    def get_bank_service(self) -> BankService:
        return self._bank_service



class ATMDemo:
    @staticmethod
    def main():
        atm = ATM.get_instance()
        
        # Perform Check Balance operation
        atm.insert_card("1234-5678-9012-3456")
        atm.enter_pin("1234")
        atm.select_operation(OperationType.CHECK_BALANCE)  # $1000
        
        # Perform Withdraw Cash operation
        atm.insert_card("1234-5678-9012-3456")
        atm.enter_pin("1234")
        atm.select_operation(OperationType.WITHDRAW_CASH, 570)
        
        # Perform Deposit Cash operation
        atm.insert_card("1234-5678-9012-3456")
        atm.enter_pin("1234")
        atm.select_operation(OperationType.DEPOSIT_CASH, 200)
        
        # Perform Check Balance operation
        atm.insert_card("1234-5678-9012-3456")
        atm.enter_pin("1234")
        atm.select_operation(OperationType.CHECK_BALANCE)  # $630
        
        # Perform Withdraw Cash more than balance
        atm.insert_card("1234-5678-9012-3456")
        atm.enter_pin("1234")
        atm.select_operation(OperationType.WITHDRAW_CASH, 700)  # Insufficient balance
        
        # Insert Incorrect PIN
        atm.insert_card("1234-5678-9012-3456")
        atm.enter_pin("3425")

if __name__ == "__main__":
    ATMDemo.main()
