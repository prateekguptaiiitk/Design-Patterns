from abc import ABC, abstractmethod
from collections import defaultdict

class ILetter(ABC):
    @abstractmethod
    def display(self, row, col):
        pass

class DocumentCharacter(ILetter):
    def __init__(self, character, font_type, size):
        self.character = character
        self.font_type = font_type
        self.size = size
    
    def get_type(self):
        return self.font_type
    
    def get_body(self):
        return self.character

    def display(self, row, col):
        print('Character:', self.character, 'font:', self.font_type, 
              'Size:', self.size, 'At position (x, y):', row, col)

class LetterFactory:
    character_cache = defaultdict(ILetter)

    @classmethod
    def create_letter(cls, character_value):  # Use 'cls' convention
        if character_value in cls.character_cache:
            return cls.character_cache[character_value]
        
        character_obj = DocumentCharacter(character_value, 'Arial', 10)
        cls.character_cache[character_value] = character_obj
        return character_obj

if __name__ == '__main__':
    '''
        This is the data we want to write into word processing

        Total = 58 characters
        t = 7 times
        h = 3 times
        a = 3 times and so on...
    '''
    
    obj1 = LetterFactory.create_letter('t')
    obj1.display(0, 0)  # Character: t font: Arial Size: 10 At position (x, y): 0 0

    obj2 = LetterFactory.create_letter('t')  # Returns cached object
    obj2.display(0, 6)  # Same object, different position
