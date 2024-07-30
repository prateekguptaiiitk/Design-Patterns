class Address:
    def __init__(self, pin_code, city, state):
        self.pin_code = pin_code
        self.city = city
        self.state = state
    
    # getters & setters methods
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

from abc import ABC, abstractmethod
class PaymentMode(ABC):
    @abstractmethod
    def makePayment(self):
        pass

class CardPaymentMode(PaymentMode):
    def make_payment(self):
        return True

class UPIPaymentMode(PaymentMode):
    def make_payment(self):
        return True

from collections import defaultdict
class Cart:
    def __init__(self):
        self.product_category_id_vs_count_map = defaultdict(int)

    # add item to cart
    def add_item_in_cart(self, product_category_id, count):
        if product_category_id in self.product_category_id_vs_count_map:
            self.product_category_id_vs_count_map[product_category_id] += count
        else:
            self.product_category_id_vs_count_map[product_category_id] = count

    # remove item to cart
    def remove_item_from_cart(self, product_category_id, count):
        if product_category_id in self.product_category_id_vs_count_map:
            no_of_items_in_cart = self.product_category_id_vs_count_map[product_category_id]
            if count - no_of_items_in_cart == 0:
                self.product_category_id_vs_count_map.pop(product_category_id)
            else:
                self.product_category_id_vs_count_map[product_category_id] = no_of_items_in_cart - count
            
    # empty my cart
    def empty_cart(self):
        self.product_category_id_vs_count_map = defaultdict(int)

    # View Cart
    def get_cart_items(self):
        return self.product_category_id_vs_count_map

class Inventory:
    def __init__(self):
        # category wise products storage
        self.product_category_list = []

    # add new category
    def add_category(self, category_id, name, price):
        productCategory = ProductCategory()
        productCategory.price = price
        productCategory.category_name = name
        productCategory.product_category_id = category_id
        self.product_category_list.append(productCategory)


    # add product to the particular category
    def add_product(self, product, product_category_id):
        # take out the respective productCategory Object
        category_object = None
        for category in self.product_category_list:
            if category.product_category_id == product_category_id:
                category_object = category
    
        if category_object != None:
            category_object.addProduct(product)

    # remove product from the category
    def remove_items(self, product_category_and_count_map):
        for category_id, count in product_category_and_count_map.items():
            category = self.get_product_category_from_id(category_id)
            category.remove_product(count)

    def get_product_category_from_id(self, product_category_id):
        for product_category in self.product_category_list:
            if product_category.product_category_id == product_category_id:
                return product_category

        return None

class Invoice:
    total_item_price = 0
    total_tax = 0
    total_final_price = 0

    # generate Invoice
    def generate_invoice(self, order):
        # it will compute and update the above details
        self.total_item_price = 200
        self.total_tax = 20
        self.total_final_price = 220