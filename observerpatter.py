from __future__ import annotations
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
	def set_stock_count(self, newStockAdded):
		pass

	@abstractmethod
	def get_stock_count(self):
		pass

class IphoneObservable(StockObservable):
	stock_count = 0
	observers = []

	def add(self, observer):
		self.observers.append(observer)

	def remove(self, observer):
		self.observers.remove(observer)

	def notify_subscriber(self):
		for observer in self.observers:
			observer.update()

	def set_stock_count(self, new_stock_added):
		if self.stock_count == 0:
			self.notify_subscriber()

		self.stock_count += new_stock_added

	def get_stock_count(self):
		return self.stock_count

class NotificationAlertObserver(ABC):
	@abstractmethod
	def update(self):
		pass

class EmailAlertObserver(NotificationAlertObserver):
	_emailId = ''
	_observable = None

	def __init__(self, email_id, observable):
		self._observable = observable
		self.email_id = email_id

	def update(self):
		self.send_message(self.email_id, 'product is back in stock')

	def send_message(self, email_id, msg):
		print('email sent to:', email_id)

class MobileAlertObserver(NotificationAlertObserver):
	mobile_no = ''
	observable = None

	def __init__(self, mobile_no, observable):
		self.observable = observable
		self.mobile_no = mobile_no

	def update(self):
		self.send_message(self.mobile_no, 'product is back in stock')

	def send_message(self, mobile_no, msg):
		print('msg sent to mobile no.:', mobile_no)

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

	iphone_stock_observable.set_stock_count(40)
	print('Current stock count:', iphone_stock_observable.get_stock_count())