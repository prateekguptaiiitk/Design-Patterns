from abc import ABC, abstractmethod
from enum import Enum

class ExpenseSplit(ABC):
    @abstractmethod
    def validate_split_request(self, split_list, total_amount):
        pass

class EqualExpenseSplit(ExpenseSplit):
    def validate_split_request(self, split_list, total_amount):
        # validate total amount in splits of each user is equal and overall equals to totalAmount
        amount_should_be_present = total_amount // len(split_list)

        for split in split_list:
            if split.get_amount_owe() != amount_should_be_present:
                raise Exception('Invalid split amount')

class UnequalExpenseSplit(ExpenseSplit):
    def validate_split_request(self, split_list, total_amount):
        return 

class PercentageExpenseSplit(ExpenseSplit):
    def validate_split_request(self, split_list, total_amount):
        return 
    
class Split:
    def __init__(self, user, amount):
        self.user = user
        self.amount_owe = amount

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user
    
    def get_amount_owe(self):
        return self.amount_owe
    
    def set_amount_owe(self, amount):
        self.amount_owe = amount

class Expense:
    def __init__(self, expense_id, description, expense_amount, paid_by_user, split_type, split_details):
        self.expense_id = expense_id
        self.description = description
        self.expense_amount = expense_amount
        self.paid_by_user = paid_by_user
        self.split_type = split_type
        self.split_details = split_details

class ExpenseController:
    def __init__(self):
        self.balance_sheet_controller = BalanceSheetController()

    def create_expense(self, expense_id, description, expense_amount, paid_by_user, split_type, split_details):
        expense_split = SplitFactory().get_split_object(split_type)
        expense_split.validate_split_request(split_details, expense_amount)
        expense = Expense(expense_id, description, expense_amount, paid_by_user, split_type, split_details)

        self.balance_sheet_controller.update_user_expense_balance_sheet(paid_by_user, split_details, expense_amount)

        return expense

class ExpenseSplitType(Enum):
    EQUAL = 'EQUAL'
    UNEQUAL = 'UNEQUAL'
    PERCENTAGE = 'PERCENTAGE'

class SplitFactory:
    def get_split_object(self, split_type):
        if split_type == ExpenseSplitType.EQUAL:
            return EqualExpenseSplit()
        elif split_type == ExpenseSplitType.UNEQUAL:
            return UnequalExpenseSplit()
        elif split_type == ExpenseSplitType.PERCENTAGE:
            return PercentageExpenseSplit()
        else:
            return None

class Group:
    def __init__(self):
        self.group_id = None
        self.group_name = None
        self.group_members = []
        self.expense_list = []
        self.expense_controller = ExpenseController()

    # add member to group
    def add_member(self, member):
        self.group_members.append(member)

    def get_group_id(self):
        return self.group_id
    
    def set_group_id(self, group_id):
        self.group_id = group_id

    def set_group_name(self, group_name):
        self.group_name = group_name
    
    def create_expense(self, expense_id, description, expense_amount, paid_by_user, split_type, split_details):
        expense = self.expense_controller.create_expense(expense_id, description, expense_amount, paid_by_user, split_type, split_details)
        self.expense_list.append(expense)
        return expense

class GroupController:
    def __init__(self):
        self.group_list = []

    # create group
    def create_new_group(self, group_id, group_name, created_by_user):
        group = Group()
        group.set_group_id(group_id)
        group.set_group_name(group_name)
        group.add_member(created_by_user)
        self.group_list.append(group)

    def get_group(self, group_id):
        for group in self.group_list:
            if group.get_group_id() == group_id:
                return group
        return None

class User:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
        self.user_expense_balance_sheet = UserExpenseBalanceSheet()
    
    def get_user_id(self):
        return self.user_id
    
    def get_user_expense_balance_sheet(self):
        return self.user_expense_balance_sheet

class UserController:
    def __init__(self):
        self.user_list = []

    # Add user
    def add_user(self, user):
        self.user_list.append(user)
    
    def get_user(self, user_id):
        for user in self.user_list:
            if user.get_user_id() == user_id:
                return user
        return None
    
    def get_all_users(self):
        return self.user_list

class Balance:
    def __init__(self):
        self.amount_owe = 0.0
        self.amount_get_back = 0.0

    def get_amount_owe(self):
        return self.amount_owe

    def set_amount_owe(self, amount_owe):
        self.amount_owe = amount_owe
    
    def get_amount_get_back(self):
        return self.amount_get_back
    
    def set_amount_get_back(self, amount_get_back):
        self.amount_get_back = amount_get_back

class BalanceSheetController:
    def update_user_expense_balance_sheet(self, expense_paid_by, splits, total_expense_amount):
        # Update the total amount paid of the expense paid by user
        paid_by_user_expense_sheet = expense_paid_by.get_user_expense_balance_sheet()
        paid_by_user_expense_sheet.set_total_payment(paid_by_user_expense_sheet.get_total_payment() + total_expense_amount)

        for split in splits:
            user_owe = split.get_user()
            owe_user_expense_sheet = user_owe.get_user_expense_balance_sheet()
            owe_amount = split.get_amount_owe()

            if expense_paid_by.get_user_id() == user_owe.get_user_id():
                paid_by_user_expense_sheet.set_total_your_expense(paid_by_user_expense_sheet.get_total_your_expense() + owe_amount)
            else:
                # Update the balance of paid user
                paid_by_user_expense_sheet.set_total_you_get_back(paid_by_user_expense_sheet.get_total_you_get_back() + owe_amount)

                if user_owe.get_user_id() in paid_by_user_expense_sheet.get_user_vs_balance():
                    user_owe_balance = paid_by_user_expense_sheet.get_user_vs_balance()[user_owe.get_user_id()]
                else:
                    user_owe_balance = Balance()
                    paid_by_user_expense_sheet.get_user_vs_balance()[user_owe.get_user_id()] = user_owe_balance

                user_owe_balance.set_amount_get_back(user_owe_balance.get_amount_get_back() + owe_amount)

                # Update the balance sheet of owe user
                owe_user_expense_sheet.set_total_you_owe(owe_user_expense_sheet.get_total_you_owe() + owe_amount)
                owe_user_expense_sheet.set_total_your_expense(owe_user_expense_sheet.get_total_your_expense() + owe_amount)

                if expense_paid_by.get_user_id() in owe_user_expense_sheet.get_user_vs_balance():
                    user_paid_balance = owe_user_expense_sheet.get_user_vs_balance()[expense_paid_by.get_user_id()]
                else:
                    user_paid_balance = Balance()
                    owe_user_expense_sheet.get_user_vs_balance()[expense_paid_by.get_user_id()] = user_paid_balance

                user_paid_balance.set_amount_owe(user_paid_balance.get_amount_owe() + owe_amount)

    def show_balance_sheet_of_user(self, user):
        print("---------------------------------------")
        print("Balance sheet of user:", user.get_user_id())

        user_expense_balance_sheet = user.get_user_expense_balance_sheet()
        print("TotalYourExpense:", user_expense_balance_sheet.get_total_your_expense())
        print("TotalGetBack:", user_expense_balance_sheet.get_total_you_get_back())
        print("TotalYourOwe:", user_expense_balance_sheet.get_total_you_owe())
        print("TotalPaymentMade:", user_expense_balance_sheet.get_total_payment())

        for user_id, balance in user_expense_balance_sheet.get_user_vs_balance().items():
            print("userID:", user_id, "YouGetBack:", balance.get_amount_get_back(), "YouOwe:", balance.get_amount_owe())

        print("---------------------------------------")

class Splitwise:
    def __init__(self):
        self.user_controller = UserController()
        self.group_controller = GroupController()
        self.balance_sheet_controller = BalanceSheetController()

    def demo(self):
        self.setup_user_and_group()

        # Step 1: Add members to the group
        group = self.group_controller.get_group("G1001")
        group.add_member(self.user_controller.get_user("U2001"))
        group.add_member(self.user_controller.get_user("U3001"))

        # Step 2: Create an expense inside a group
        splits = []
        split1 = Split(self.user_controller.get_user("U1001"), 300)
        split2 = Split(self.user_controller.get_user("U2001"), 300)
        split3 = Split(self.user_controller.get_user("U3001"), 300)
        splits.append(split1)
        splits.append(split2)
        splits.append(split3)
        group.create_expense("Exp1001", "Breakfast", 900, self.user_controller.get_user("U1001"), ExpenseSplitType.EQUAL, splits)

        splits2 = []
        splits2_1 = Split(self.user_controller.get_user("U1001"), 400)
        splits2_2 = Split(self.user_controller.get_user("U2001"), 100)
        splits2.append(splits2_1)
        splits2.append(splits2_2)
        group.create_expense("Exp1002", "Lunch", 500, self.user_controller.get_user("U2001"), ExpenseSplitType.UNEQUAL, splits2)

        for user in self.user_controller.get_all_users():
            self.balance_sheet_controller.show_balance_sheet_of_user(user)

    def setup_user_and_group(self):
        # Onboard user to splitwise app
        self.add_users_to_splitwise_app()

        # Create a group by user1
        user1 = self.user_controller.get_user("U1001")
        self.group_controller.create_new_group("G1001", "Outing with Friends", user1)

    def add_users_to_splitwise_app(self):
        # Adding User1
        user1 = User("U1001", "User1")

        # Adding User2
        user2 = User("U2001", "User2")

        # Adding User3
        user3 = User("U3001", "User3")

        self.user_controller.add_user(user1)
        self.user_controller.add_user(user2)
        self.user_controller.add_user(user3)

class UserExpenseBalanceSheet:
    def __init__(self):
        self.user_vs_balance = {}
        self.total_your_expense = 0
        self.total_payment = 0
        self.total_you_owe = 0
        self.total_you_get_back = 0

    def get_user_vs_balance(self):
        return self.user_vs_balance

    def get_total_your_expense(self):
        return self.total_your_expense

    def set_total_your_expense(self, total_your_expense):
        self.total_your_expense = total_your_expense

    def get_total_you_owe(self):
        return self.total_you_owe

    def set_total_you_owe(self, total_you_owe):
        self.total_you_owe = total_you_owe

    def get_total_you_get_back(self):
        return self.total_you_get_back

    def set_total_you_get_back(self, total_you_get_back):
        self.total_you_get_back = total_you_get_back

    def get_total_payment(self):
        return self.total_payment

    def set_total_payment(self, total_payment):
        self.total_payment = total_payment

if __name__ == '__main__':
    splitwise = Splitwise()
    splitwise.demo()
