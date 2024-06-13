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
	def notifySubscriber(self):
		pass

	@abstractmethod
	def setStockCount(self, newStockAdded):
		pass

	@abstractmethod
	def getStockCount(self):
		pass

class IphoneObservable(StockObservable):

	_stockCount = 0
	_observers = []

	def add(self, observer):
		self._observers.append(observer)

	def remove(self, observer):
		self._observers.remove(observer)

	def notifySubscriber(self):
		for observer in self._observers:
			observer.update()

	def setStockCount(self, newStockAdded):
		if self._stockCount == 0:
			self.notifySubscriber()

		self._stockCount += newStockAdded

	def getStockCount(self):
		return self._stockCount


class NotificationAlertObserver(ABC):

	@abstractmethod
	def update(self):
		pass


class EmailAlertObserver(NotificationAlertObserver):
	_emailId = ''
	_observable = None

	def __init__(self, emailId, observable):
		self._observable = observable
		self._emailId = emailId

	def update(self):
		self.sendMessage(self._emailId, 'product is back in stock')

	def sendMessage(self, emailId, msg):
		print('email sent to:', emailId)

class MobileAlertObserver(NotificationAlertObserver):
	_mobileNo = ''
	_observable = None

	def __init__(self, mobileNo, observable):
		self._observable = observable
		self._mobileNo = mobileNo

	def update(self):
		self.sendMessage(self._mobileNo, 'product is back in stock')

	def sendMessage(self, mobileNo, msg):
		print('msg sent to mobile no.:', mobileNo)

if __name__ == '__main__':
	iphoneStockObservable = IphoneObservable()
	observer1 = EmailAlertObserver('abc@gmail.com', iphoneStockObservable)
	observer2 = EmailAlertObserver('xyz@gmail.com', iphoneStockObservable)
	observer3 = MobileAlertObserver('1122334455', iphoneStockObservable)

	iphoneStockObservable.add(observer1)
	iphoneStockObservable.add(observer2)
	iphoneStockObservable.add(observer3)

	iphoneStockObservable.setStockCount(10)
	iphoneStockObservable.setStockCount(-10)

	iphoneStockObservable.remove(observer2)

	iphoneStockObservable.setStockCount(40)
	print('Current stock count:', iphoneStockObservable.getStockCount())