// ILetter Interface (abstract base)
class ILetter {
  display(row, col) {
    throw new Error("Method 'display()' must be implemented.");
  }
}

// Concrete Flyweight
class DocumentCharacter extends ILetter {
  constructor(character, fontType, size) {
    super();
    this.character = character;
    this.fontType = fontType;
    this.size = size;
  }

  display(row, col) {
    console.log(
      `Character: ${this.character}, font: ${this.fontType}, Size: ${this.size}, At position (x, y): ${row}, ${col}`
    );
  }
}

// Flyweight Factory
class LetterFactory {
  static characterCache = new Map();

  static createLetter(characterValue) {
    if (this.characterCache.has(characterValue)) {
      return this.characterCache.get(characterValue);
    }

    const characterObj = new DocumentCharacter(characterValue, 'Ariel', 10);
    this.characterCache.set(characterValue, characterObj);
    return characterObj;
  }
}

// Client Code
const obj1 = LetterFactory.createLetter('t');
obj1.display(0, 0);

const obj2 = LetterFactory.createLetter('t');
obj2.display(0, 6);
