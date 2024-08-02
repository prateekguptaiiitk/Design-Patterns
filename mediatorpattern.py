from abc import ABC, abstractmethod

class Colleague(ABC):
    @abstractmethod
    def place_bid(self, bid_amount):
        pass

    def receive_bid_notification(self, bid_amount):
        pass

    def get_name(self):
        pass

class Bidder(Colleague):
    def __init__(self, name, auction_mediator):
        self.name = name
        self.auction_mediator = auction_mediator
        self.auction_mediator.add_bidder(self)

    def place_bid(self, bid_amount):
        self.auction_mediator.place_bid(self, bid_amount)

    def receive_bid_notification(self, bid_amount):
        print('Bidder:', self.name, 'got notification that someone has put a bid of:', bid_amount)

    def get_name(self):
        return self.name
    
# this is a mediator interface
class AuctionMediator(ABC):
    @abstractmethod
    def add_bidder(self, bidder):
        pass

    @abstractmethod
    def place_bid(self, bidder, bid_amount):
        pass

class Auction(AuctionMediator):
    def __init__(self):
        self.colleagues = []

    def add_bidder(self, bidder):
        self.colleagues.append(bidder)

    def place_bid(self, bidder, bid_amount):
        for colleague in self.colleagues:
            if colleague.get_name() != bidder.get_name():
                colleague.receive_bid_notification(bid_amount)

if __name__ == '__main__':
    auction_mediator_obj = Auction()
    bidder_1 = Bidder('A', auction_mediator_obj)
    bidder_2 = Bidder('B', auction_mediator_obj)

    bidder_1.place_bid(2000)
    bidder_2.place_bid(3000)
    bidder_1.place_bid(3001)
