from abc import ABC, abstractmethod

# adaptee
class WeighingMachine(ABC):
    
    @abstractmethod
    def getWeightInPound(self):
        pass

class WeighingMachineForBabies(WeighingMachine):
    def __init__(self, weight):
        self.weight = weight

    def getWeightInPound(self):
        return self.weight
    
# adapter
class WeighingMachineAdapter(ABC):
    
    @abstractmethod
    def getWeightInKg(self):
        pass

class WeighingMachineAdapterImpl(WeighingMachineAdapter):

    def __init__(self, weighingMachine):
        self.weighingMachine = weighingMachine
    
    def getWeightInKg(self):
        weightInPound = self.weighingMachine.getWeightInPound()

        # Convert it to KGs
        weightInKg = weightInPound * 0.453592
        return weightInKg

# client
if __name__ == '__main__':
    weighingMachineAdapter = WeighingMachineAdapterImpl(WeighingMachineForBabies(50))
    print(weighingMachineAdapter.getWeightInKg())
