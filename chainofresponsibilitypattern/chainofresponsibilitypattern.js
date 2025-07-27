// ===== Enum for Log Levels =====
const LogLevel = Object.freeze({
  INFO: 1,
  DEBUG: 2,
  ERROR: 3,
});

// ===== Abstract Log Processor =====
class LogProcessor {
  constructor(nextLoggerProcessor) {
    this.nextLoggerProcessor = nextLoggerProcessor;
  }

  log(logLevel, message) {
    if (this.nextLoggerProcessor) {
      this.nextLoggerProcessor.log(logLevel, message);
    }
  }
}

// ===== Concrete Info Logger =====
class InfoLogProcessor extends LogProcessor {
  constructor(nextLoggerProcessor) {
    super(nextLoggerProcessor);
  }

  log(logLevel, message) {
    if (logLevel === LogLevel.INFO) {
      console.log('INFO: ', message);
    } else {
      super.log(logLevel, message);
    }
  }
}

// ===== Concrete Debug Logger =====
class DebugLogProcessor extends LogProcessor {
  constructor(nextLoggerProcessor) {
    super(nextLoggerProcessor);
  }

  log(logLevel, message) {
    if (logLevel === LogLevel.DEBUG) {
      console.log('DEBUG: ', message);
    } else {
      super.log(logLevel, message);
    }
  }
}

// ===== Concrete Error Logger =====
class ErrorLogProcessor extends LogProcessor {
  constructor(nextLoggerProcessor) {
    super(nextLoggerProcessor);
  }

  log(logLevel, message) {
    if (logLevel === LogLevel.ERROR) {
      console.log('ERROR: ', message);
    } else {
      super.log(logLevel, message);
    }
  }
}

// ===== Client Code =====
const logObject = new InfoLogProcessor(
  new DebugLogProcessor(
    new ErrorLogProcessor(null)
  )
);

logObject.log(LogLevel.ERROR, "exception happens");
// ERROR:  exception happens

logObject.log(LogLevel.DEBUG, "need to debug this");
// DEBUG:  need to debug this

logObject.log(LogLevel.INFO, "just for info");
// INFO:  just for info
