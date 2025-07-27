// Abstract class
class PaymentFlow {
  sendMoney() {
    this.validateRequest();
    this.debitAmount();
    this.calculateFees();
    this.creditAmount();
  }

  validateRequest() {
    throw new Error('Method "validateRequest" must be implemented');
  }

  debitAmount() {
    throw new Error('Method "debitAmount" must be implemented');
  }

  calculateFees() {
    throw new Error('Method "calculateFees" must be implemented');
  }

  creditAmount() {
    throw new Error('Method "creditAmount" must be implemented');
  }
}

class PayToFriend extends PaymentFlow {
  validateRequest() {
    console.log('Validate logic of PayToFriend');
  }

  debitAmount() {
    console.log('Debit the amount logic of PayToFriend');
  }

  calculateFees() {
    console.log('0% fees charged');
  }

  creditAmount() {
    console.log('Credit the full amount');
  }
}

class PayToMerchant extends PaymentFlow {
  validateRequest() {
    console.log('Validate logic of PayToMerchant');
  }

  debitAmount() {
    console.log('Debit the amount logic of PayToMerchant');
  }

  calculateFees() {
    console.log('2% fees charged');
  }

  creditAmount() {
    console.log('Credit the remaining amount');
  }
}

// Usage
const payToFriend = new PayToFriend();
payToFriend.sendMoney();

console.log('---');

const payToMerchant = new PayToMerchant();
payToMerchant.sendMoney();
