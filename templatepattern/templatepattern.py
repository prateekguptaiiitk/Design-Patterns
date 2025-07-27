from abc import ABC, abstractmethod

class PaymentFlow(ABC):
    @abstractmethod
    def validate_request(self):
        pass

    @abstractmethod
    def calculate_fees(self):
        pass

    @abstractmethod
    def debit_amount(self):
        pass
    
    @abstractmethod
    def credit_amount(self):
        pass

    # this is Template method: which defines the order of steps to execute the task
    def send_money(self):
        # step-1
        self.validate_request()

        # step-2
        self.debit_amount()

        # step-3
        self.calculate_fees()

        # step-4
        self.credit_amount()

class PayToFriend(PaymentFlow):
    def validate_request(self):
        # specific validation for PayToFriend flow
        print('Validate logic of PayToFriend')

    def debit_amount(self):
        # debit the amount
        print('Debit the amount logic of PayToFriend')
    
    def calculate_fees(self):
        # specific fee computation logic for PayToFriend flow
        print('0% fees charged')
    
    def credit_amount(self):
        # credit the amount logic
        print('Credit the full amount')
    
class PayToMerchant(PaymentFlow):
    def validate_request(self):
        # specific validation for PayToMerchant flow
        print('Validate logic of PayToMerchant')

    def debit_amount(self):
        # debit the amount
        print('Debit the amount logic of PayToMerchant')
    
    def calculate_fees(self):
        # specific fee computation logic for PayToMerchant flow
        print('2% fees charged')
    
    def credit_amount(self):
        # credit the amount logic
        print('Credit the remaining amount')

if __name__ == '__main__':
    pay_to_friend = PayToFriend()
    pay_to_friend.send_money()