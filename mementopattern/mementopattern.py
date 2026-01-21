# originator
class ConfigurationOriginator:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_width(self, width):
        self.width = width
    
    def create_memento(self):
        return ConfigurationMemento(self.height, self.width)
    
    def restore_memento(self, memento):
        self.height, self.width = memento._get_state()

# memento
class ConfigurationMemento:
    def __init__(self, height, width):
        self.__height = height
        self.__width = width
    
    def _get_state(self):
        return self.__height, self.__width
    
# caretaker
class ConfigurationCareTaker:
    def __init__(self):
        self.history = []

    def save(self, memento):
        self.history.append(memento)
    
    def get_last_memento(self):
        if self.history:
            # get and remove the last memento from the list
            last_memento = self.history.pop()

            return last_memento
    
        return None

if __name__ == '__main__':
    caretaker = ConfigurationCareTaker()
    originator = ConfigurationOriginator(5, 10)

    # save it
    snapshot_1 = originator.create_memento()

    # add it to history
    caretaker.save(snapshot_1)

    # originator changing to new state
    originator.set_height(7)
    originator.set_width(12)

    # save it
    snapshot_2 = originator.create_memento()

    # add it to history
    caretaker.save(snapshot_2)

    # originator changing to new state
    originator.set_height(9)
    originator.set_width(14)

    # UNDO
    restored_state_memento_obj = caretaker.get_last_memento()
    originator.restore_memento(restored_state_memento_obj)
    
    print('height:', originator.height, 'width:', originator.width)
    
    restored_state_memento_obj = caretaker.get_last_memento()
    originator.restore_memento(restored_state_memento_obj)
    
    print('height:', originator.height, 'width:', originator.width)
