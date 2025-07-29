// ===== Singleton: URLShortener =====
class URLShortener {
  constructor(encoder) {
    if (URLShortener._instance) {
        return URLShortener._instance;
    }

    this.encoder = encoder;
    this.urlMap = new Map();  // short -> long
    this.reverseMap = new Map(); // long -> short

    URLShortener._instance = this;
  }

  shorten(longUrl) {
    if (this.reverseMap.has(longUrl)) {
      return this.reverseMap.get(longUrl);
    }

    const shortCode = this.encoder.encode(longUrl);
    this.urlMap.set(shortCode, longUrl);
    this.reverseMap.set(longUrl, shortCode);
    return shortCode;
  }

  retrieve(shortCode) {
    return this.urlMap.get(shortCode);
  }
}

class Encoder {
    encode(longUrl) {
        throw new Error('implement abstract method encode()')
    }
}

// ===== Base62 Encoder =====
class Base62Encoder extends Encoder{
  constructor() {
    super()
    this.counter = 100000; // ensures uniqueness
    this.charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  }

  encode(longUrl) {
    return this.encodeBase62(this.counter++);
  }

  encodeBase62(num) {
    let base = this.charset.length;
    let result = '';
    while (num > 0) {
      result = this.charset[num % base] + result;
      num = Math.floor(num / base);
    }
    return result || '0';
  }
}

// ===== UUID Encoder (alternative strategy) =====
class UUIDEncoder extends Encoder{
  encode(longUrl) {
    return 'xxxxxxx'.replace(/x/g, () =>
      Math.floor(Math.random() * 36).toString(36)
    );
  }
}

// ===== Factory: EncoderFactory =====
class EncoderFactory {
  static getEncoder(type) {
    switch (type) {
      case 'base62':
        return new Base62Encoder();
      case 'uuid':
        return new UUIDEncoder();
      default:
        throw new Error(`Encoder not found for type: ${type}`);
    }
  }
}

// Use base62 encoder via factory
const encoder = EncoderFactory.getEncoder('base62');
const shortener = new URLShortener(encoder);

const short1 = shortener.shorten('https://openai.com/research');
console.log('Short:', short1); // e.g., 'q0E'
console.log('Original:', shortener.retrieve(short1)); // 'https://openai.com/research'

const short2 = shortener.shorten('https://github.com');
console.log('Short:', short2); // e.g., 'q0F'
console.log('Original:', shortener.retrieve(short2)); // 'https://github.com'
