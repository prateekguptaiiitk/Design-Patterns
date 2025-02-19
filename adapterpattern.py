from abc import ABC, abstractmethod

# adaptee
class WeightMaching(ABC):
    
    @abstractmethod
    def getWeightInPound(self):
        pass

class WeightMachineForBabies(WeightMaching):
    def getWeightInPound(self):
        weight = int(input('Enter weight in pounds: '))
        return weight
    
# adapter
class WeightMachineAdapter(ABC):
    
    @abstractmethod
    def getWeightInKg(self):
        pass

class WeightMachineAdapterImpl(WeightMachineAdapter):

    def __init__(self, weightMachine):
        self.weightMachine = weightMachine
    
    def getWeightInKg(self):
        weightInPound = self.weightMachine.getWeightInPound()

        # Convert it to KGs
        weightInKg = weightInPound * 0.45
        return weightInKg

# client
if __name__ == '__main__':
    weightMachineAdapter = WeightMachineAdapterImpl(WeightMachineForBabies())
    print(weightMachineAdapter.getWeightInKg())
