from abc import ABC, abstractmethod

class StockObservable(ABC):
    @abstractmethod
    def add(self, observer):
        pass

    @abstractmethod
    def remove(self, observer):
        pass

    @abstractmethod
    def notify_subscriber(self):
        pass

    @abstractmethod
    def set_stock_count(self, new_stock_added):
        pass

    @abstractmethod
    def get_stock_count(self):
        pass

class IphoneObservable(StockObservable):
    def __init__(self):
        self.stock_count = 0
        self.observers = []

    def add(self, observer):
        self.observers.append(observer)

    def remove(self, observer):
        self.observers.remove(observer)

    def notify_subscriber(self):
        for observer in self.observers:
            observer.update()

    def set_stock_count(self, new_stock_added):
        prev_stock = self.stock_count
        self.stock_count += new_stock_added

        if prev_stock == 0 and self.stock_count > 0:
            self.notify_subscriber()

    def get_stock_count(self):
        return self.stock_count

class NotificationAlertObserver(ABC):
    @abstractmethod
    def update(self):
        pass

class EmailAlertObserver(NotificationAlertObserver):
    def __init__(self, email_id, observable):
        self.observable = observable
        self.email_id = email_id

    def update(self):
        if self.observable.get_stock_count() > 0:
            self.send_email('product is back in stock')

    def send_email(self, msg):
        print('email sent to:', self.email_id)

class MobileAlertObserver(NotificationAlertObserver):
    def __init__(self, mobile_no, observable):
        self.observable = observable
        self.mobile_no = mobile_no

    def update(self):
        if self.observable.get_stock_count() <= 5:
            self.send_message("Hurry! Only few left")

    def send_message(self, msg):
        print(msg)
        print('msg sent to mobile no.:', self.mobile_no)

if __name__ == '__main__':
    iphone_stock_observable = IphoneObservable()
    observer1 = EmailAlertObserver('abc@gmail.com', iphone_stock_observable)
    observer2 = EmailAlertObserver('xyz@gmail.com', iphone_stock_observable)
    observer3 = MobileAlertObserver('1122334455', iphone_stock_observable)

    iphone_stock_observable.add(observer1)
    iphone_stock_observable.add(observer2)
    iphone_stock_observable.add(observer3)

    iphone_stock_observable.set_stock_count(10)
    iphone_stock_observable.set_stock_count(-10)

    iphone_stock_observable.remove(observer2)

    iphone_stock_observable.set_stock_count(5)
    print('Current stock count:', iphone_stock_observable.get_stock_count())
