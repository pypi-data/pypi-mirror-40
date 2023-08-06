from .Box import Box
from sumer import YearMonth, Timer

from datetime import datetime, timedelta
import aenum

class UsagePeriod(aenum.MultiValueEnum):
	DAY = 'day', 'days', 'Day', 'Days'
	MONTH = 'month', 'months', 'Month', 'Months'

	def __repr__(self):
		return self.value

	@property
	def plural(self):
		return self.value+'s'


class UsageMeter:
	def __init__(self, id, name=None, period=UsagePeriod.DAY, wait_time=None, limit=None, box=None, path=None):
		"""
		:type period: UsagePeriod
		:type box: Box
		:type path: str
		"""
		self._id = id
		self._name = name
		if type(period) is not UsagePeriod: period = UsagePeriod(period)
		self._usage = {}
		self._period = period
		self._last_used = None
		self._limit = limit
		self._wait_time = wait_time

		if box is None and path is not None:
			self._box = Box(path=path)
		else:
			self._box = box

		# put self into the box
		if self._box.contains(self._id):
			# get all the usage from the box
			other = self._box.get(self._id)
			self.merge(other)
			# replace the old usage with self
		self._box.put(name=self._id, obj=self)


	@property
	def id(self):
		return self._id

	@property
	def usage(self):
		return self._usage.copy()

	def get_usage(self, add_id=False):
		usage_dict = self.usage
		if add_id:
			usage_dict['id']=self.id
			usage_dict['last_used']=self.last_used
		return usage_dict

	def get_this_period_usage(self):
		if self.timestamp in self._usage:
			return self._usage[self.timestamp]
		else:
			return 0

	def is_limit_reached(self):
		if self._limit is None:
			return False
		return self.get_this_period_usage()>=self._limit

	def is_waited_enough(self):
		if self._wait_time is None:
			return True
		return self.get_elapsed()>=self._wait_time

	def is_ready(self):
		if self._last_used is None:
			return True
		return self.is_waited_enough() and not self.is_limit_reached()

	@property
	def timestamp(self):
		if self._period == UsagePeriod.DAY:
			return datetime.today().date()
		elif self._period == UsagePeriod.MONTH:
			today = datetime.today()
			return YearMonth(year=today.year, month=today.month)

	def get_elapsed(self):
		delta = datetime.now() - self.last_used
		return delta.seconds + delta.microseconds/1E6

	def use(self):
		if self.timestamp in self._usage:
			self._usage[self.timestamp] += 1
		else:
			self._usage[self.timestamp] = 1
		self._last_used = datetime.now()
		return self._id

	@property
	def last_used(self):
		if self._last_used is None:
			return datetime.now() - timedelta(days=365)
		return self._last_used



	def merge(self, other):
		"""
		:type other: UsageMeter
		"""
		for key, usage in other._usage.items():
			if key in self._usage:
				self._usage[key] += usage
			else:
				self._usage[key] = usage
		if self._last_used is None:
			self._last_used = other._last_used
		else:
			self._last_used = max(self._last_used, other._last_used)

	def flush(self):
		self._box.flush()

	def save(self):
		self._box.save()

	def __repr__(self):
		if self._name is None:
			name = ''
		else:
			name = self._name + ' : '
		return f'{name}{self._id}'





