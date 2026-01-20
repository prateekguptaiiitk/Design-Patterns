from abc import ABC, abstractmethod

class Aggregate(ABC):
    @abstractmethod
    def create_iterator(self):
        pass

class Library(Aggregate):
    def __init__(self, book_list):
        self.book_list = book_list

    def create_iterator(self):
        return BookIterator(self.book_list)
    
class IteratorInterface(ABC):
    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

class BookIterator(IteratorInterface):
    def __init__(self, books):
        self.books = books
        self.index = 0

    def has_next(self):
        return self.index < len(self.books)
    
    def next(self):
        if self.has_next():
            book = self.books[self.index]
            self.index += 1
            return book
        
        return None

class Book:
    def __init__(self, price, book_name):
        self.price = price
        self.book_name = book_name
    
    def get_price(self):
        return self.price
    
    def get_book_name(self):
        return self.book_name

if __name__ == '__main__':
    book_list = [
        Book(100, 'Science'),
        Book(200, 'Maths'),
        Book(300, 'GK'),
        Book(400, 'Drawing')
    ]

    lib = Library(book_list)
    iterator = lib.create_iterator()

    while iterator.has_next():
        book = iterator.next()
        print(book.get_book_name())
