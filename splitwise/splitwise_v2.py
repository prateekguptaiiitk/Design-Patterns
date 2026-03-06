import threading
from typing import Dict, List, Optional
from datetime import datetime
import uuid
from abc import ABC, abstractmethod


class BalanceSheet:
    def __init__(self, owner: 'User'):
        self._owner = owner
        self._balances: Dict['User', float] = {}
        self._lock = threading.Lock()
    
    def get_balances(self) -> Dict['User', float]:
        # if we don't use .copy() - This breaks encapsulation because external code can modify balances.
        return self._balances.copy()
    
    def adjust_balance(self, other_user: 'User', amount: float):
        with self._lock:
            if self._owner == other_user:
                return  # Cannot owe yourself
            
            if other_user in self._balances:
                self._balances[other_user] += amount
            else:
                self._balances[other_user] = amount
    
    def show_balances(self):
        print(f"--- Balance Sheet for {self._owner.get_name()} ---")
        if not self._balances:
            print("All settled up!")
            return
        
        total_owed_to_me = 0
        total_i_owe = 0
        
        for other_user, amount in self._balances.items():
            if amount > 0.01:
                print(f"{other_user.get_name()} owes {self._owner.get_name()} ${amount:.2f}")
                total_owed_to_me += amount
            elif amount < -0.01:
                print(f"{self._owner.get_name()} owes {other_user.get_name()} ${-amount:.2f}")
                total_i_owe += (-amount)
        
        print(f"Total Owed to {self._owner.get_name()}: ${total_owed_to_me:.2f}")
        print(f"Total {self._owner.get_name()} Owes: ${total_i_owe:.2f}")
        print("---------------------------------")


class User:
    def __init__(self, name: str, email: str):
        self._id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._balance_sheet = BalanceSheet(self)
    
    def get_id(self) -> str:
        return self._id
    
    def get_name(self) -> str:
        return self._name
    
    def get_balance_sheet(self) -> 'BalanceSheet':
        return self._balance_sheet


class Split:
    def __init__(self, user: 'User', amount: float):
        self._user = user
        self._amount = amount
    
    def get_user(self) -> 'User':
        return self._user
    
    def get_amount(self) -> float:
        return self._amount


# interface
class SplitStrategy(ABC):
    @abstractmethod
    def calculate_splits(self, total_amount: float, paid_by: 'User', participants: List['User'], split_values: Optional[List[float]]) -> List['Split']:
        pass

class EqualSplitStrategy(SplitStrategy):
    def calculate_splits(self, total_amount: float, paid_by: 'User', participants: List['User'], split_values: Optional[List[float]]) -> List['Split']:
        splits = []
        amount_per_person = total_amount / len(participants)
        for participant in participants:
            splits.append(Split(participant, amount_per_person))
        return splits

class ExactSplitStrategy(SplitStrategy):
    def calculate_splits(self, total_amount: float, paid_by: 'User', participants: List['User'], split_values: Optional[List[float]]) -> List['Split']:
        if len(participants) != len(split_values):
            raise ValueError("Number of participants and split values must match.")
        if abs(sum(split_values) - total_amount) > 0.01:
            raise ValueError("Sum of exact amounts must equal the total expense amount.")
        
        splits = []
        for i in range(len(participants)):
            splits.append(Split(participants[i], split_values[i]))
        return splits

class PercentageSplitStrategy(SplitStrategy):
    def calculate_splits(self, total_amount: float, paid_by: 'User', participants: List['User'], split_values: Optional[List[float]]) -> List['Split']:
        if len(participants) != len(split_values):
            raise ValueError("Number of participants and split values must match.")
        if abs(sum(split_values) - 100.0) > 0.01:
            raise ValueError("Sum of percentages must be 100.")
        
        splits = []
        for i in range(len(participants)):
            amount = (total_amount * split_values[i]) / 100.0
            splits.append(Split(participants[i], amount))
        return splits



class Expense:
    def __init__(self, builder: 'ExpenseBuilder'):
        self._id = builder._id or str(uuid.uuid4())
        self._description = builder._description
        self._amount = builder._amount
        self._paid_by = builder._paid_by
        self._timestamp = datetime.now()
        
        # Use the strategy to calculate splits
        self._splits = builder._split_strategy.calculate_splits(
            builder._amount, builder._paid_by, builder._participants, builder._split_values
        )
    
    def get_id(self) -> str:
        return self._id
    
    def get_description(self) -> str:
        return self._description
    
    def get_amount(self) -> float:
        return self._amount
    
    def get_paid_by(self) -> User:
        return self._paid_by
    
    def get_splits(self) -> List[Split]:
        return self._splits
    
    class ExpenseBuilder:
        def __init__(self):
            self._id: Optional[str] = None
            self._description: Optional[str] = None
            self._amount: Optional[float] = None
            self._paid_by: Optional[User] = None
            self._participants: Optional[List[User]] = None
            self._split_strategy: Optional[SplitStrategy] = None
            self._split_values: Optional[List[float]] = None
        
        def set_id(self, expense_id: str) -> 'Expense.ExpenseBuilder':
            self._id = expense_id
            return self
        
        def set_description(self, description: str) -> 'Expense.ExpenseBuilder':
            self._description = description
            return self
        
        def set_amount(self, amount: float) -> 'Expense.ExpenseBuilder':
            self._amount = amount
            return self
        
        def set_paid_by(self, paid_by: User) -> 'Expense.ExpenseBuilder':
            self._paid_by = paid_by
            return self
        
        def set_participants(self, participants: List[User]) -> 'Expense.ExpenseBuilder':
            self._participants = participants
            return self
        
        def set_split_strategy(self, split_strategy: SplitStrategy) -> 'Expense.ExpenseBuilder':
            self._split_strategy = split_strategy
            return self
        
        def set_split_values(self, split_values: List[float]) -> 'Expense.ExpenseBuilder':
            self._split_values = split_values
            return self
        
        def build(self) -> 'Expense':
            if self._split_strategy is None:
                raise ValueError("Split strategy is required.")
            return Expense(self)


class Group:
    def __init__(self, name: str, members: List['User']):
        self._id = str(uuid.uuid4())
        self._name = name
        self._members = members
    
    def get_id(self) -> str:
        return self._id
    
    def get_name(self) -> str:
        return self._name
    
    def get_members(self) -> List['User']:
        return self._members.copy()


class Transaction:
    def __init__(self, from_user: 'User', to_user: 'User', amount: float):
        self._from = from_user
        self._to = to_user
        self._amount = amount
    
    def __str__(self) -> str:
        return f"{self._from.get_name()} should pay {self._to.get_name()} ${self._amount:.2f}"



class SplitwiseService:
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
            self._users: Dict[str, User] = {}
            self._groups: Dict[str, Group] = {}
            self._initialized = True
    
    @classmethod
    def get_instance(cls):
        return cls()
    
    def add_user(self, name: str, email: str) -> User:
        user = User(name, email)
        self._users[user.get_id()] = user
        return user
    
    def add_group(self, name: str, members: List[User]) -> Group:
        group = Group(name, members)
        self._groups[group.get_id()] = group
        return group
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def get_group(self, group_id: str) -> Optional[Group]:
        return self._groups.get(group_id)
    
    def create_expense(self, builder: Expense.ExpenseBuilder):
        with self._lock:
            expense = builder.build()
            paid_by = expense.get_paid_by()
            
            for split in expense.get_splits():
                participant = split.get_user()
                amount = split.get_amount()
                
                if paid_by != participant:
                    paid_by.get_balance_sheet().adjust_balance(participant, amount)
                    participant.get_balance_sheet().adjust_balance(paid_by, -amount)
            
            print(f"Expense '{expense.get_description()}' of amount {expense.get_amount()} created.")
    
    def settle_up(self, payer_id: str, payee_id: str, amount: float):
        with self._lock:
            payer = self._users[payer_id]
            payee = self._users[payee_id]
            print(f"{payer.get_name()} is settling up {amount} with {payee.get_name()}")
            
            # Settlement is like a reverse expense. payer owes less to payee.
            payee.get_balance_sheet().adjust_balance(payer, -amount)
            payer.get_balance_sheet().adjust_balance(payee, amount)
    
    def show_balance_sheet(self, user_id: str):
        user = self._users[user_id]
        user.get_balance_sheet().show_balances()
    
    def simplify_group_debts(self, group_id: str) -> List[Transaction]:
        group = self._groups.get(group_id)
        if group is None:
            raise ValueError("Group not found")
        
        # Calculate net balance for each member within the group context
        net_balances = {}
        for member in group.get_members():
            balance = 0
            for other_user, amount in member.get_balance_sheet().get_balances().items():
                # Consider only balances with other group members
                if other_user in group.get_members():
                    balance += amount
            net_balances[member] = balance
        
        # Separate into creditors and debtors
        creditors = [(user, balance) for user, balance in net_balances.items() if balance > 0]
        debtors = [(user, balance) for user, balance in net_balances.items() if balance < 0]
        
        creditors.sort(key=lambda x: x[1], reverse=True)
        debtors.sort(key=lambda x: x[1])
        
        transactions = []
        i = j = 0
        
        while i < len(creditors) and j < len(debtors):
            creditor_user, creditor_amount = creditors[i]
            debtor_user, debtor_amount = debtors[j]
            
            amount_to_settle = min(creditor_amount, -debtor_amount)
            transactions.append(Transaction(debtor_user, creditor_user, amount_to_settle))
            
            creditors[i] = (creditor_user, creditor_amount - amount_to_settle)
            debtors[j] = (debtor_user, debtor_amount + amount_to_settle)
            
            if abs(creditors[i][1]) < 0.01:
                i += 1
            if abs(debtors[j][1]) < 0.01:
                j += 1
        
        return transactions


class SplitwiseDemo:
    @staticmethod
    def main():
        # 1. Setup the service
        service = SplitwiseService.get_instance()
        
        # 2. Create users and groups
        alice = service.add_user("Alice", "alice@a.com")
        bob = service.add_user("Bob", "bob@b.com")
        charlie = service.add_user("Charlie", "charlie@c.com")
        david = service.add_user("David", "david@d.com")
        
        friends_group = service.add_group("Friends Trip", [alice, bob, charlie, david])
        
        print("--- System Setup Complete ---\n")
        
        # 3. Use Case 1: Equal Split
        print("--- Use Case 1: Equal Split ---")
        service.create_expense(Expense.ExpenseBuilder()
                              .set_description("Dinner")
                              .set_amount(1000)
                              .set_paid_by(alice)
                              .set_participants([alice, bob, charlie, david])
                              .set_split_strategy(EqualSplitStrategy()))
        
        service.show_balance_sheet(alice.get_id())
        service.show_balance_sheet(bob.get_id())
        print()
        
        # 4. Use Case 2: Exact Split
        print("--- Use Case 2: Exact Split ---")
        service.create_expense(Expense.ExpenseBuilder()
                              .set_description("Movie Tickets")
                              .set_amount(370)
                              .set_paid_by(alice)
                              .set_participants([bob, charlie])
                              .set_split_strategy(ExactSplitStrategy())
                              .set_split_values([120.0, 250.0]))
        
        service.show_balance_sheet(alice.get_id())
        service.show_balance_sheet(bob.get_id())
        print()
        
        # 5. Use Case 3: Percentage Split
        print("--- Use Case 3: Percentage Split ---")
        service.create_expense(Expense.ExpenseBuilder()
                              .set_description("Groceries")
                              .set_amount(500)
                              .set_paid_by(david)
                              .set_participants([alice, bob, charlie])
                              .set_split_strategy(PercentageSplitStrategy())
                              .set_split_values([40.0, 30.0, 30.0]))  # 40%, 30%, 30%
        
        print("--- Balances After All Expenses ---")
        service.show_balance_sheet(alice.get_id())
        service.show_balance_sheet(bob.get_id())
        service.show_balance_sheet(charlie.get_id())
        service.show_balance_sheet(david.get_id())
        print()
        
        # 6. Use Case 4: Simplify Group Debts
        print("--- Use Case 4: Simplify Group Debts for 'Friends Trip' ---")
        simplified_debts = service.simplify_group_debts(friends_group.get_id())
        if not simplified_debts:
            print("All debts are settled within the group!")
        else:
            for debt in simplified_debts:
                print(debt)
        print()
        
        service.show_balance_sheet(bob.get_id())
        
        # 7. Use Case 5: Partial Settlement
        print("--- Use Case 5: Partial Settlement ---")
        # From the simplified debts, we see Bob should pay Alice. Let's say Bob pays 100.
        service.settle_up(bob.get_id(), alice.get_id(), 100)
        
        print("--- Balances After Partial Settlement ---")
        service.show_balance_sheet(alice.get_id())
        service.show_balance_sheet(bob.get_id())

if __name__ == "__main__":
    SplitwiseDemo.main()
