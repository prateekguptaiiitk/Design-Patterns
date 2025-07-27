from abc import ABC, abstractmethod

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
        return self.type
    
    def get_body(self):
        return self.body

    def display(self, row, col):
        # use character of a particular font type and size at a given location
        print('Character:', self.character, 'font:', self.font_type, 'Size:', self.size, 'At position (x, y):', row, col)

from collections import defaultdict
class LetterFactory:
    character_cache = defaultdict(ILetter)

    @classmethod
    def create_letter(self, character_value):
        if character_value in self.character_cache:
            return self.character_cache[character_value]
        
        character_obj = DocumentCharacter(character_value, 'Ariel', 10)
        self.character_cache[character_value] = character_obj
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
    obj1.display(0, 0)

    obj2 = LetterFactory.create_letter('t')
    obj2.display(0, 6)