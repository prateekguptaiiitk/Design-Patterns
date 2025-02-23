from enum import Enum

class LogType(Enum):
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
        if log_level == LogType.INFO:
            print('INFO: ', message)
        else:
            super().log(log_level, message)

class DebugLogProcessor(LogProcessor):
    def __init__(self, next_logger_processor):
        super().__init__(next_logger_processor)

    def log(self, log_level, message):
        if log_level == LogType.DEBUG:
            print('DEBUG: ', message)
        else:
            super().log(log_level, message)

class ErrorLogProcessor(LogProcessor):
    def __init__(self, next_logger_processor):
        super().__init__(next_logger_processor)

    def log(self, log_level, message):
        if log_level == LogType.ERROR:
            print('ERROR: ', message)
        else:
            super().log(log_level, message)

if __name__ == '__main__':
    logObject = InfoLogProcessor(DebugLogProcessor(ErrorLogProcessor(None)))

    logObject.log(LogType.ERROR, "exception happens")
    logObject.log(LogType.DEBUG, "need to debug this ")
    logObject.log(LogType.INFO, "just for info ")
