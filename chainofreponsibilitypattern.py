class LogProcessor:
	INFO = 1
	DEBUG = 2
	ERROR = 3

	nextLoggerProcessor = None

	def __init__(self, loggerProcessor):
		self.nextLoggerProcessor = loggerProcessor

	def log(self, loglevel, message):
		if self.nextLoggerProcessor:
			self.nextLoggerProcessor.log(loglevel, message)

class InfoLogProcessor(LogProcessor):
	def __init__(self, nextLoggerProcessor):
		super().__init__(nextLoggerProcessor)

	def log(self, loglevel, message):
		if loglevel == self.INFO:
			print('INFO: ', message)
		else:
			super().log(loglevel, message)

class DebugLogProcessor(LogProcessor):
	def __init__(self, nextLoggerProcessor):
		super().__init__(nextLoggerProcessor)

	def log(self, loglevel, message):
		if loglevel == self.DEBUG:
			print('DEBUG: ', message)
		else:
			super().log(loglevel, message)

class ErrorLogProcessor(LogProcessor):
	def __init__(self, nextLoggerProcessor):
		super().__init__(nextLoggerProcessor)

	def log(self, loglevel, message):
		if loglevel == self.ERROR:
			print('ERROR: ', message)
		else:
			super().log(loglevel, message)

if __name__ == '__main__':
	logObject = InfoLogProcessor(DebugLogProcessor(ErrorLogProcessor(None)))

	logObject.log(LogProcessor.ERROR, "exception happens")
	logObject.log(LogProcessor.DEBUG, "need to debug this ")
	logObject.log(LogProcessor.INFO, "just for info ")
