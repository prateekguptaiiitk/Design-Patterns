from enum import Enum

class LogLevel(Enum):
    INFO = 1
    DEBUG = 2
    ERROR = 3
    
class LogProcessor:
    def __init__(self, logger_processor):
        self.next_logger_processor = logger_processor

    def log(self, log_level, message):
        if self.next_logger_processor:
            self.next_logger_processor.log(log_level, message)

class InfoLogProcessor(LogProcessor):
    def __init__(self, next_logger_processor):
        super().__init__(next_logger_processor)

    def log(self, log_level, message):
        if log_level == LogLevel.INFO:
            print('INFO: ', message)
        else:
            super().log(log_level, message)

class DebugLogProcessor(LogProcessor):
    def __init__(self, next_logger_processor):
        super().__init__(next_logger_processor)

    def log(self, log_level, message):
        if log_level == LogLevel.DEBUG:
            print('DEBUG: ', message)
        else:
            super().log(log_level, message)

class ErrorLogProcessor(LogProcessor):
    def __init__(self, next_logger_processor):
        super().__init__(next_logger_processor)

    def log(self, log_level, message):
        if log_level == LogLevel.ERROR:
            print('ERROR: ', message)
        else:
            super().log(log_level, message)

if __name__ == '__main__':
    logObject = InfoLogProcessor(DebugLogProcessor(ErrorLogProcessor(None)))

    logObject.log(LogLevel.ERROR, "exception happens")
    logObject.log(LogLevel.DEBUG, "need to debug this ")
    logObject.log(LogLevel.INFO, "just for info ")
