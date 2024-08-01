from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum

class Address:
    def __init__(self, pin_code, city, state):
        self.pin_code = pin_code
        self.city = city
        self.state = state

    def get_pincode(self):
        return self.pin_code

    def set_pincode(self, pin_code):
        self.pin_code = pin_code

    def get_city(self):
        return self.city

    def set_city(self, city):
        self.city = city

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def __str__(self):
        return f"Address(pin_code={self.pin_code}, city={self.city}, state={self.state})"


class PaymentMode(ABC):
    @abstractmethod
    def make_payment(self):
        pass

class CardPaymentMode(PaymentMode):
    def make_payment(self):
        return True

class UPIPaymentMode(PaymentMode):
    def make_payment(self):
        return True


class Cart:
    def __init__(self):
        self.product_category_id_vs_count_map = defaultdict(int)

    def add_item_in_cart(self, product_category_id, count):
        if product_category_id in self.product_category_id_vs_count_map:
            self.product_category_id_vs_count_map[product_category_id] += count
        else:
            self.product_category_id_vs_count_map[product_category_id] = count

    def remove_item_from_cart(self, product_category_id, count):
        if product_category_id in self.product_category_id_vs_count_map:
            no_of_items_in_cart = self.product_category_id_vs_count_map[product_category_id]
            if count >= no_of_items_in_cart:
                self.product_category_id_vs_count_map.pop(product_category_id)
            else:
                self.product_category_id_vs_count_map[product_category_id] = no_of_items_in_cart - count

    def empty_cart(self):
        self.product_category_id_vs_count_map = defaultdict(int)

    def get_cart_items(self):
        return self.product_category_id_vs_count_map

    def __str__(self):
        return f"Cart(items={dict(self.product_category_id_vs_count_map)})"


class Inventory:
    def __init__(self):
        self.product_category_list = []

    def add_category(self, category_id, name, price):
        product_category = ProductCategory()
        product_category.price = price
        product_category.category_name = name
        product_category.product_category_id = category_id
        self.product_category_list.append(product_category)

    def add_product(self, product, product_category_id):
        category_object = None
        for category in self.product_category_list:
            if category.product_category_id == product_category_id:
                category_object = category

        if category_object is not None:
            category_object.add_product(product)

    def remove_items(self, product_category_and_count_map):
        for category_id, count in product_category_and_count_map.items():
            category = self.get_product_category_from_id(category_id)
            category.remove_product(count)

    def get_product_category_from_id(self, product_category_id):
        for product_category in self.product_category_list:
            if product_category.product_category_id == product_category_id:
                return product_category
        return None

    def __str__(self):
        categories = "\n".join(str(category) for category in self.product_category_list)
        return f"Inventory(categories:\n{categories})"


class Invoice:
    def __init__(self):
        self.total_item_price = 0
        self.total_tax = 0
        self.total_final_price = 0

    def generate_invoice(self, order):
        self.total_item_price = 200
        self.total_tax = 20
        self.total_final_price = 220

    def __str__(self):
        return f"Invoice(total_item_price={self.total_item_price}, total_tax={self.total_tax}, total_final_price={self.total_final_price})"


class WarehouseSelectionStrategy(ABC):
    @abstractmethod
    def select_warehouse(self, warehouse_list):
        pass

class NearestWarehouseSelectionStrategy(WarehouseSelectionStrategy):
    def select_warehouse(self, warehouse_list):
        return warehouse_list[0]


class Order:
    def __init__(self, user, warehouse):
        self.user = user
        self.product_category_and_count_map = user.get_user_cart().get_cart_items()
        self.warehouse = warehouse
        self.delivery_address = user.address
        self.invoice = Invoice()
        self.invoice.generate_invoice(self)
        self.payment = None
        self.order_status = None

    def checkout(self):
        print("Checkout process started.")
        self.warehouse.remove_item_from_inventory(self.product_category_and_count_map)
        is_payment_success = self.make_payment(UPIPaymentMode())

        if is_payment_success:
            print("Payment successful. Emptying cart...")
            self.user.get_user_cart().empty_cart()
        else:
            print("Payment failed. Restoring items to inventory...")
            self.warehouse.add_item_to_inventory(self.product_category_and_count_map)

    def make_payment(self, payment_mode):
        payment = Payment(payment_mode)
        return payment.make_payment()

    def generate_order_invoice(self):
        self.invoice.generate_invoice(self)

    def __str__(self):
        return f"Order(user_id={self.user.user_id}, warehouse_id={id(self.warehouse)}, address={self.delivery_address})"


class OrderController:
    def __init__(self):
        self.order_list = []
        self.user_IDVs_orders = defaultdict(list)

    def create_new_order(self, user, warehouse):
        order = Order(user, warehouse)
        self.order_list.append(order)
        self.user_IDVs_orders[user.user_id].append(order)
        return order

    def remove_order(self, order):
        print('Order removed successfully')

    def get_order_by_customer_id(self, user_id):
        return None

    def get_order_by_order_id(self, user_id):
        return None


class OrderStatus(Enum):
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'
    RETURNED = 'RETURNED'
    UNDELIVERED = 'UNDELIVERED'


class Payment:
    def __init__(self, payment_mode):
        self.payment_mode = payment_mode

    def make_payment(self):
        return self.payment_mode.make_payment()


class Product:
    def __init__(self):
        self.product_id = None
        self.product_name = None

    def __str__(self):
        return f"Product(product_id={self.product_id}, product_name={self.product_name})"


class ProductCategory:
    def __init__(self):
        self.product_category_id = 0
        self.category_name = None
        self.products = []
        self.price = 0.0

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, count):
        for _ in range(count):
            if self.products:
                self.products.pop()

    def get_products(self):
        return self.products

    def __str__(self):
        products = ", ".join(str(product) for product in self.products)
        return f"ProductCategory(id={self.product_category_id}, name={self.category_name}, price={self.price}, products=[{products}])"


class ProductDeliverySystem:
    def __init__(self, user_list, warehouse_list):
        self.user_controller = UserController(user_list)
        self.warehouse_controller = WarehouseController(warehouse_list, None)
        self.order_controller = OrderController()

    def get_user(self, user_id):
        return self.user_controller.get_user(user_id)

    def get_warehouse(self, warehouse_selection_strategy):
        return self.warehouse_controller.select_warehouse(warehouse_selection_strategy)

    def get_inventory(self, warehouse):
        return warehouse.inventory

    def add_product_to_cart(self, user, product, count):
        cart = user.get_user_cart()
        cart.add_item_in_cart(product.product_category_id, count)

    def place_order(self, user, warehouse):
        return self.order_controller.create_new_order(user, warehouse)

    def checkout(self, order):
        order.checkout()


class User:
    def __init__(self):
        self.user_cart_details = Cart()
        self.order_ids = []
        self.user_id = None
        self.user_name = None
        self.address = None

    def get_user_cart(self):
        return self.user_cart_details

    def __str__(self):
        return f"User(user_id={self.user_id}, user_name={self.user_name}, address={self.address})"


class UserController:
    def __init__(self, user_list):
        self.user_list = user_list

    def add_user(self, user):
        self.user_list.append(user)

    def remove_user(self, user):
        self.user_list.remove(user)

    def get_user(self, user_id):
        for user in self.user_list:
            if user.user_id == user_id:
                return user
        return None


class Warehouse:
    def __init__(self):
        self.inventory = None
        self.address = None

    def remove_item_from_inventory(self, product_category_and_count_map):
        self.inventory.remove_items(product_category_and_count_map)

    def add_item_to_inventory(self, product_category_and_count_map):
        pass

    def __str__(self):
        return f"Warehouse(address={self.address}, inventory={self.inventory})"


class WarehouseController:
    def __init__(self, warehouse_list, warehouse_selection_strategy):
        self.warehouse_list = warehouse_list
        self.warehouse_selection_strategy = warehouse_selection_strategy

    def add_new_warehouse(self, warehouse):
        self.warehouse_list.add(warehouse)

    def remove_warehouse(self, warehouse):
        self.warehouse_list.remove(warehouse)

    def select_warehouse(self, selection_strategy):
        self.warehouse_selection_strategy = selection_strategy
        return self.warehouse_selection_strategy.select_warehouse(self.warehouse_list)


class Main:
    def main(self):
        print("Initializing Main...")
        warehouse_list = [self.add_warehouse_and_its_inventory()]
        user_list = [self.create_user()]

        product_delivery_system = ProductDeliverySystem(user_list, warehouse_list)
        self.run_delivery_flow(product_delivery_system, 1)

    def add_warehouse_and_its_inventory(self):
        warehouse = Warehouse()
        inventory = Inventory()

        inventory.add_category(1, "Peppsii Large Cold Drink", 100)
        inventory.add_category(4, "Doovee small Soap", 50)

        product1 = Product()
        product1.product_id = 1
        product1.product_name = "Peepsii"

        product2 = Product()
        product2.product_id = 2
        product2.product_name = "Peepsii"

        product3 = Product()
        product3.product_id = 3
        product3.product_name = "Doovee"

        inventory.add_product(product1, 1)
        inventory.add_product(product2, 1)
        inventory.add_product(product3, 4)

        warehouse.inventory = inventory
        print(f"Added Warehouse: {warehouse}")
        return warehouse

    def create_user(self):
        user = User()
        user.user_id = 1
        user.user_name = "SJ"
        user.address = Address(230011, "city", "state")
        print(f"Created User: {user}")
        return user

    def run_delivery_flow(self, product_delivery_system, user_id):
        user = product_delivery_system.get_user(user_id)
        print(f"Retrieved User: {user}")

        warehouse = product_delivery_system.get_warehouse(NearestWarehouseSelectionStrategy())
        print(f"Selected Warehouse: {warehouse}")

        inventory = product_delivery_system.get_inventory(warehouse)
        print(f"Retrieved Inventory: {inventory}")

        product_category_i_want_to_order = None
        for product_category in inventory.product_category_list:
            if product_category.category_name == "Peppsii Large Cold Drink":
                product_category_i_want_to_order = product_category

        print(f"Product Category Selected: {product_category_i_want_to_order}")
        product_delivery_system.add_product_to_cart(user, product_category_i_want_to_order, 2)
        print(f"Cart after adding product: {user.get_user_cart()}")

        order = product_delivery_system.place_order(user, warehouse)
        print(f"Order placed: {order}")

        product_delivery_system.checkout(order)
        print(f"Order after checkout: {order}")


if __name__ == '__main__':
    main = Main()
    main.main()
