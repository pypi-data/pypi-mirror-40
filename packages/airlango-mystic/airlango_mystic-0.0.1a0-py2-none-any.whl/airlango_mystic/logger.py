import datetime
import threading

LOG_LV_DEBUG = 1
LOG_LV_INFO = 2
LOG_LV_WARN = 3
LOG_LV_ERROR = 4
LOG_LV_ALL = 0
LOG_LV_NONE = 100

class Logger:
	def __init__(self, tag='n/a', level=LOG_LV_INFO):
		self.log_level = level
		self.tag = tag
		self.lock = threading.Lock()

	def ts_str(self):
		now = datetime.datetime.now()
		ts = ("%04d-%02d-%02d %02d:%02d:%02d.%03d"
				% (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond / 1000))
		return "%s" % (ts)

	def set_tag(self, tag):
		self.tag = tag

	def set_level(self, level):
		self.log_level = level

	def output(self, msg):
		self.lock.acquire()
		print(msg)
		self.lock.release()

	def error(self, str):
		if self.log_level <= LOG_LV_ERROR:
			self.output("%s E <%s> %s" % (self.ts_str(), self.tag, str))

	def warn(self, str):
		if self.log_level <= LOG_LV_WARN:
			self.output("%s W <%s> %s" % (self.ts_str(), self.tag, str))

	def info(self, str):
		if self.log_level <= LOG_LV_INFO:
			self.output("%s I <%s> %s" % (self.ts_str(), self.tag, str))

	def debug(self, str):
		if self.log_level <= LOG_LV_DEBUG:
			self.output("%s D <%s> %s" % (self.ts_str(), self.tag, str))
