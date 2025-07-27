// Abstract Aggregate
class Aggregate {
  createIterator() {
    throw new Error('Method "createIterator()" must be implemented.');
  }
}

// Concrete Aggregate
class Library extends Aggregate {
  constructor(bookList) {
    super();
    this.bookList = bookList;
  }

  createIterator() {
    return new BookIterator(this.bookList);
  }
}

// Abstract Iterator
class Iterator {
  hasNext() {
    throw new Error('Method "hasNext()" must be implemented.');
  }

  next() {
    throw new Error('Method "next()" must be implemented.');
  }
}

// Concrete Iterator
class BookIterator extends Iterator {
  constructor(books) {
    super();
    this.books = books;
    this.index = 0;
  }

  hasNext() {
    return this.index < this.books.length;
  }

  next() {
    if (this.hasNext()) {
      const book = this.books[this.index];
      this.index += 1;
      return book;
    }
    return null;
  }
}

// Book class
class Book {
  constructor(price, bookName) {
    this.price = price;
    this.bookName = bookName;
  }

  getPrice() {
    return this.price;
  }

  getBookName() {
    return this.bookName;
  }
}

// Client code
const bookList = [
  new Book(100, 'Science'),
  new Book(200, 'Maths'),
  new Book(300, 'GK'),
  new Book(400, 'Drawing')
];

const lib = new Library(bookList);
const iterator = lib.createIterator();

while (iterator.hasNext()) {
  const book = iterator.next();
  console.log(book.getBookName());
}
