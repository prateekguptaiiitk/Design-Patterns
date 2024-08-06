from abc import ABC, abstractmethod

class RoomElement(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class SingleRoom(RoomElement):
    def __init__(self):
        self.room_price = 0
    
    def accept(self, visitor):
        visitor.visit(self)

class DoubleRoom(RoomElement):
    def __init__(self):
        self.room_price = 0
    
    def accept(self, visitor):
        visitor.visit(self)

class DeluxRoom(RoomElement):
    def __init__(self):
        self.room_price = 0
    
    def accept(self, visitor):
        visitor.visit(self)

class RoomVisitor(ABC):
    @abstractmethod
    def visit(self, room):
        pass

class RoomPricingVisitor(RoomVisitor):
    def visit(self, room):
        if isinstance(room, SingleRoom):
            print('Pricing computation logic of single room')
            room.room_price = 1000
        elif isinstance(room, DoubleRoom):
            print('Pricing computation logic of double room')
            room.room_price = 2000
        elif isinstance(room, DeluxRoom):
            print('Pricing computation logic of delux room')
            room.room_price = 3000

class RoomMaintenanceVisitor(RoomVisitor):
    def visit(self, room):
        if isinstance(room, SingleRoom):
            print('Performing maintenance of single room')
        elif isinstance(room, DoubleRoom):
            print('Performing maintenance of double room')
        elif isinstance(room, DeluxRoom):
            print('Performing maintenance of delux room')

if __name__ == '__main__':
    single_room_obj = SingleRoom()
    double_room_obj = DoubleRoom()
    delux_room_obj = DeluxRoom()

    # performing an operation on the objects
    pricing_visitor_obj = RoomPricingVisitor()

    single_room_obj.accept(pricing_visitor_obj)
    print(single_room_obj.room_price)

    double_room_obj.accept(pricing_visitor_obj)
    print(double_room_obj.room_price)

    delux_room_obj.accept(pricing_visitor_obj)
    print(delux_room_obj.room_price)

    # performing another operation on the objects
    maintenance_visitor_obj = RoomMaintenanceVisitor()
    single_room_obj.accept(maintenance_visitor_obj)

    double_room_obj.accept(maintenance_visitor_obj)

    delux_room_obj.accept(maintenance_visitor_obj)