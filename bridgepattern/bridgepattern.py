from abc import ABC, abstractmethod

class LivingThings(ABC):
    def __init__(self, breathe_implementor):
        self.breathe_implementor = breathe_implementor
    
    @abstractmethod
    def breathe_process(self):
        pass

class Dog(LivingThings):
    def __init__(self, breathe_implementor):
        super().__init__(breathe_implementor)
    
    def breathe_process(self):
        self.breathe_implementor.breathe()

class Fish(LivingThings):
    def __init__(self, breathe_implementor):
        super().__init__(breathe_implementor)
    
    def breathe_process(self):
        self.breathe_implementor.breathe()

class Tree(LivingThings):
    def __init__(self, breathe_implementor):
        super().__init__(breathe_implementor)
    
    def breathe_process(self):
        self.breathe_implementor.breathe()

class BreatheImplementor(ABC):
    @abstractmethod
    def breathe(self):
        pass

class LandBreatheImplementation(BreatheImplementor):
    def breathe(self):
        print('breathes through nose')
        print('inhale oxygen from air')
        print('exhale carbon dioxide')

class WaterBreatheImplementation(BreatheImplementor):
    def breathe(self):
        print('breathes through gills')
        print('inhale oxygen from water')
        print('exhale carbon dioxide')

class TreeBreatheImplementation(BreatheImplementor):
    def breathe(self):
        print('breathes through leaves')
        print('inhale carbon dioxide')
        print('exhale oxygen through photosynthesis')

if __name__ == '__main__':
    fish_obj = Fish(WaterBreatheImplementation())
    fish_obj.breathe_process()

    tree_obj = Tree(TreeBreatheImplementation())
    tree_obj.breathe_process()