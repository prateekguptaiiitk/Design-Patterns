class ProductDAO:
    def get_product(self, productID):
        # get product based on product id and return it
        print('Product with ID = ', productID)
        return productID

class Payment:
    def make_payment(self):
        return True

class Invoice:
    def generate_invoice(self):
        # this will generate the invoice
        print('invoice generated')

class SendNotification:
    def send_notification(self):
        # this will send notification to clients
        print('notification sent')

class OrderFacade:
    def __init__(self):
        self.productDAO = ProductDAO()
        self.invoice = Invoice()
        self.payment = Payment()
        self.notification = SendNotification()
    
    def create_order(self):
        product = self.productDAO.get_product(121)
        self.payment.make_payment()
        self.invoice.generate_invoice()
        self.notification.send_notification()
        # order creation successfull
        print('Order created successfully!')

class OrderClient:
    @classmethod
    def main(self):
        order_facade = OrderFacade()
        order_facade.create_order()

if __name__ == '__main__':
    OrderClient.main()
