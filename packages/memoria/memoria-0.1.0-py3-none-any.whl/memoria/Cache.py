from .Box import Box
from sumer import get_elapsed
from boudica import ProgressBar
from .hash_collection import make_hash_sha256
import time
from datetime import datetime
import atexit

class Cache:
	_ENCODING_BASE = 64

	def __init__(self, path='cache', days_to_expire = 30, extension='memc', num_tries=1, try_delay=0):
		self._box = Box(path=path, extension=extension)
		self._days_to_expire = days_to_expire
		self._num_tries = num_tries
		self._try_delay = try_delay

	@staticmethod
	def create_cache_dict(hashed_args=None, unhashed_args=None, func_name=None):
		hashed_args = hashed_args or {}
		unhashed_args = unhashed_args or {}

		hash_dict = hashed_args.copy()
		hash_dict['_func_name_'] = func_name
		return {
			'hashed_args': hashed_args,
			'unhashed_args': unhashed_args,
			'func_name': func_name,
			'result': None,
			'time': datetime.now(),
			'times_accessed': 0,
			'cache_key': make_hash_sha256(hash_dict)
		}

	@staticmethod
	def run_cache_dict(cache_dict, func):
		"""
		:type cache_dict: dict
		:type func: callable
		"""
		kwargs = cache_dict['unhashed_args'].copy()
		kwargs.update(cache_dict['hashed_args'])
		cache_dict['time'] = datetime.now()
		cache_dict['result'] = func(**kwargs)

	@staticmethod
	def get_simplified_dict(cache_dict):
		"""
		:type cache_dict: dict
		:rtype: dict
		"""
		result = cache_dict['hashed_args'].copy()
		result['func_name'] = cache_dict['func_name']
		result['time'] = cache_dict['time']
		result['cache_key'] = cache_dict['cache_key']
		result['times_accessed'] = cache_dict['times_accessed']
		return result


	@property
	def path(self):
		return self._box.path

	def save(self, echo=1):
		echo = max(0, echo)
		self._box.save(echo=echo)

	@classmethod
	def hash(cls, obj):
		return make_hash_sha256(obj=obj, base=cls._ENCODING_BASE)


	@property
	def cache_keys(self):
		return self._box.names

	@property
	def size(self):
		return self._box.size

	@property
	def file_size(self):
		return self._box.file_size

	def get(self, cache_key):
		result = self._box.get(name=cache_key)
		result['times_accessed'] += 1
		return result

	def contains(self, cache_key):
		return self._box.contains(name=cache_key)

	def put(self, cache_key, obj):
		self._box.put(name=cache_key, obj=obj)

	def is_expired(self, cache_key):
		cached_version = self._box.get(name=cache_key)
		elapsed = get_elapsed(start=cached_version['time'])
		return elapsed.days >= self._days_to_expire

	def remove_expired(self, progress_bar=True):
		cache_keys = list(self.cache_keys)
		actual_progress_bar = ProgressBar(total=self.size)
		progress = 0
		for cache_key in cache_keys:
			if self.is_expired(cache_key=cache_key):
				self.remove(cache_key=cache_key)
			if progress_bar:
				progress+=1
				actual_progress_bar.show(amount=progress)

	def to_list(self, simplified=True):
		if simplified:
			the_list = [self.get_simplified_dict(cache_dict) for key, cache_dict in self._box.items]
		else:
			the_list = list(self._box.objects)
		the_list.sort(key=lambda x:x['time'])
		return the_list

	def remove(self, cache_key=None):
		self._box.remove(name=cache_key)

	# takes the n cached objects from the beginning
	def remove_earliest(self, n=1):
		n = min(n, self.size)
		to_remove = self.to_list()[0:n]
		for cache_dict in to_remove:
			self.remove(cache_key=cache_dict['cache_key'])
		return to_remove

	def flush(self):
		self._box.flush()

	def cache(
			self, func, condition_func=lambda x:True, func_name=None, echo=0, hashed_args=None,
			unhashed_args=None, use_cache=True
	):
		# the arguments can either be passed through a dictionary or kwargs
		"""
		:param return_cache_key: if True, the cache key is also returned with the result
		:type func: callable
		:type condition_func: callable
		:param condition_func: a function that determines if the results are OK to be saved or not
		:type echo: int
		:type hashed_args: dict or NoneType
		:type unhashed_args: dict or NoneType
		:return: result of func(**args_dict, **kwargs)
		"""
		echo = max(0, echo)
		cache_dict = self.create_cache_dict(hashed_args=hashed_args, unhashed_args=unhashed_args, func_name=func_name)

		# from cache
		if self.contains(cache_key=cache_dict['cache_key']) and use_cache:
			cached_version = self.get(cache_key=cache_dict['cache_key'])
			if get_elapsed(start=cached_version['time']).days<self._days_to_expire:
				if echo: print(f'using the cached version for: {hashed_args}')
				cache_dict['times_accessed'] += 1
				return cached_version

		# new run
		for i in range(self._num_tries):
			self.run_cache_dict(cache_dict=cache_dict, func=func)
			if condition_func(cache_dict['result']):
				if echo: print(f'caching result of: {hashed_args}')
				self.put(cache_key=cache_dict['cache_key'], obj=cache_dict)
				return cache_dict
			time.sleep(2**i*self._try_delay)

		if echo: print(f'result of: {hashed_args} is not cachable.')
		return cache_dict


