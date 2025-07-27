// ===== Abstract Colleague =====
class Colleague {
  placeBid(bidAmount) {
    throw new Error('placeBid() must be implemented');
  }

  receiveBidNotification(bidAmount) {
    // Default empty implementation
  }

  getName() {
    throw new Error('getName() must be implemented');
  }
}

// ===== Concrete Colleague: Bidder =====
class Bidder extends Colleague {
  constructor(name, auctionMediator) {
    super();
    this.name = name;
    this.auctionMediator = auctionMediator;
    this.auctionMediator.addBidder(this);
  }

  placeBid(bidAmount) {
    this.auctionMediator.placeBid(this, bidAmount);
  }

  receiveBidNotification(bidAmount) {
    console.log(`Bidder: ${this.name} got notification that someone has put a bid of: ${bidAmount}`);
  }

  getName() {
    return this.name;
  }
}

// ===== Abstract Mediator =====
class AuctionMediator {
  addBidder(bidder) {
    throw new Error('addBidder() must be implemented');
  }

  placeBid(bidder, bidAmount) {
    throw new Error('placeBid() must be implemented');
  }
}

// ===== Concrete Mediator: Auction =====
class Auction extends AuctionMediator {
  constructor() {
    super();
    this.colleagues = [];
  }

  addBidder(bidder) {
    this.colleagues.push(bidder);
  }

  placeBid(bidder, bidAmount) {
    for (const colleague of this.colleagues) {
      if (colleague.getName() !== bidder.getName()) {
        colleague.receiveBidNotification(bidAmount);
      }
    }
  }
}

// ===== Client Code =====
const auctionMediatorObj = new Auction();
const bidder1 = new Bidder('A', auctionMediatorObj);
const bidder2 = new Bidder('B', auctionMediatorObj);

bidder1.placeBid(2000);
// Bidder: B got notification that someone has put a bid of: 2000

bidder2.placeBid(3000);
// Bidder: A got notification that someone has put a bid of: 3000

bidder1.placeBid(3001);
// Bidder: B got notification that someone has put a bid of: 3001
