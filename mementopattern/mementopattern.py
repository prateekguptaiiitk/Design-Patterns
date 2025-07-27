# originator
class ConfigurationOriginator:
    def __init__(self, height,  width):
        self.height = height
        self.width = width
    
    def set_height(self, height):
        self.height = height

    def set_width(self, width):
        self.width = width
    
    def create_memento(self):
        return ConfigurationMemento(self.height, self.width)
    
    def restore_memento(self, memento_to_be_restored):
        self.height = memento_to_be_restored.height
        self.width = memento_to_be_restored.width

# memento
class ConfigurationMemento:
    def __init__(self, height, width):
        self.height = height
        self.width = width
    
    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    
# caretaker
class ConfigurationCareTaker:
    history = []

    def add_memento(self, memento):
        self.history.append(memento)
    
    def undo(self):
        if len(self.history) != 0:
            # get and remove the last memento from the list
            last_memento = self.history.pop()

            return last_memento
    
        return None

class Client:
    care_taker_obj = ConfigurationCareTaker()

    # initiate state of the originator
    originator_obj = ConfigurationOriginator(5, 10)

    # save it
    snapshot_1 = originator_obj.create_memento()

    # add it to history
    care_taker_obj.add_memento(snapshot_1)

    # originator changing to new state
    originator_obj.set_height(7)
    originator_obj.set_width(12)

    # save it
    snapshot_2 = originator_obj.create_memento()

    # add it to history
    care_taker_obj.add_memento(snapshot_2)

    # originator changing to new state
    originator_obj.set_height(9)
    originator_obj.set_width(14)

    # UNDO
    restored_state_memento_obj = care_taker_obj.undo()
    originator_obj.restore_memento(restored_state_memento_obj)
    
    print('height:', originator_obj.height, 'width:', originator_obj.width)
    
    restored_state_memento_obj = care_taker_obj.undo()
    originator_obj.restore_memento(restored_state_memento_obj)
    
    print('height:', originator_obj.height, 'width:', originator_obj.width)

if __name__ == '__main__':
    Client()