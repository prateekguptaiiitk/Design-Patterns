class ProductDAO {
  getProduct(productID) {
    // get product based on product id and return it
    console.log("Product with ID = ", productID);
    return productID;
  }
}

class Payment {
  makePayment() {
    return true;
  }
}

class Invoice {
  generateInvoice() {
    // this will generate the invoice
    console.log("invoice generated");
  }
}

class SendNotification {
  sendNotification() {
    // this will send notification to clients
    console.log("notification sent");
  }
}

class OrderFacade {
  constructor() {
    this.productDAO = new ProductDAO();
    this.invoice = new Invoice();
    this.payment = new Payment();
    this.notification = new SendNotification();
  }

  createOrder() {
    const product = this.productDAO.getProduct(121);
    this.payment.makePayment();
    this.invoice.generateInvoice();
    this.notification.sendNotification();

    // order creation successful
    console.log("Order created successfully!");
  }
}

class OrderClient {
  static main() {
    const orderFacade = new OrderFacade();
    orderFacade.createOrder();
  }
}

OrderClient.main();
