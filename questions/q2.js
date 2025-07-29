/*
* Create a Logger using Factory Pattern
*/

// 1. Base Logger Interface
class Logger {
  log(message) {
    throw new Error("log() must be implemented by subclass");
  }
}

// 2. Concrete Logger Implementations

class ConsoleLogger extends Logger {
  log(message) {
    console.log(`[Console] ${message}`);
  }
}

class FileLogger extends Logger {
  log(message) {
    // Simulating file logging
    console.log(`[File] Writing to file: ${message}`);
  }
}

class RemoteLogger extends Logger {
  log(message) {
    // Simulating remote logging
    console.log(`[Remote] Sending log to remote server: ${message}`);
  }
}

// 3. Logger Factory
class LoggerFactory {
  static getLogger(type) {
    switch (type) {
      case "console":
        return new ConsoleLogger();
      case "file":
        return new FileLogger();
      case "remote":
        return new RemoteLogger();
      default:
        throw new Error(`Unknown logger type: ${type}`);
    }
  }
}

// 4. Usage
const logger1 = LoggerFactory.getLogger("console");
logger1.log("App started"); // [Console] App started

const logger2 = LoggerFactory.getLogger("file");
logger2.log("Something went wrong"); // [File] Writing to file: Something went wrong

const logger3 = LoggerFactory.getLogger("remote");
logger3.log("User signed in"); // [Remote] Sending log to remote server: User signed in