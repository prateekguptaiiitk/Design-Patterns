// Abstract Element
class RoomElement {
  accept(visitor) {
    throw new Error('Method "accept()" must be implemented.');
  }
}

// Concrete Elements
class SingleRoom extends RoomElement {
  constructor() {
    super();
    this.roomPrice = 0;
  }

  accept(visitor) {
    visitor.visit(this);
  }
}

class DoubleRoom extends RoomElement {
  constructor() {
    super();
    this.roomPrice = 0;
  }

  accept(visitor) {
    visitor.visit(this);
  }
}

class DeluxRoom extends RoomElement {
  constructor() {
    super();
    this.roomPrice = 0;
  }

  accept(visitor) {
    visitor.visit(this);
  }
}

// Abstract Visitor
class RoomVisitor {
  visit(room) {
    throw new Error('Method "visit()" must be implemented.');
  }
}

// Concrete Visitors
class RoomPricingVisitor extends RoomVisitor {
  visit(room) {
    if (room instanceof SingleRoom) {
      console.log('Pricing computation logic of single room');
      room.roomPrice = 1000;
    } else if (room instanceof DoubleRoom) {
      console.log('Pricing computation logic of double room');
      room.roomPrice = 2000;
    } else if (room instanceof DeluxRoom) {
      console.log('Pricing computation logic of delux room');
      room.roomPrice = 3000;
    }
  }
}

class RoomMaintenanceVisitor extends RoomVisitor {
  visit(room) {
    if (room instanceof SingleRoom) {
      console.log('Performing maintenance of single room');
    } else if (room instanceof DoubleRoom) {
      console.log('Performing maintenance of double room');
    } else if (room instanceof DeluxRoom) {
      console.log('Performing maintenance of delux room');
    }
  }
}

// Client code
const singleRoomObj = new SingleRoom();
const doubleRoomObj = new DoubleRoom();
const deluxRoomObj = new DeluxRoom();

const pricingVisitorObj = new RoomPricingVisitor();

singleRoomObj.accept(pricingVisitorObj);
console.log(singleRoomObj.roomPrice);

doubleRoomObj.accept(pricingVisitorObj);
console.log(doubleRoomObj.roomPrice);

deluxRoomObj.accept(pricingVisitorObj);
console.log(deluxRoomObj.roomPrice);

const maintenanceVisitorObj = new RoomMaintenanceVisitor();

singleRoomObj.accept(maintenanceVisitorObj);
doubleRoomObj.accept(maintenanceVisitorObj);
deluxRoomObj.accept(maintenanceVisitorObj);
