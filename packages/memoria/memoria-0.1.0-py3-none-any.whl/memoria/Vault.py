from .Box import Box
from .Crypto import Crypto
from datetime import datetime
import getpass
import random
from .get_hardware_uid import get_hardware_uid

class Vault(Box):
	def __init__(self, path, key=None, timeout=17, extension='memv'):
		super().__init__(path=path, extension=extension)
		if key is None:
			self._timeout = None
			self._key_type = 'local_id'
			self._key = get_hardware_uid()
		else:
			self._key = key
			self._key_type = 'password'
			self._timeout = timeout

		self._unlock_time = datetime.now()
		self.put(name='__random__', obj=random.random()) # to make it hard to reverse engineer and find the key

	def put(self, name, obj):
		if self.locked: self.unlock()
		crypto = Crypto(key=self._key)
		if super().contains(name='items'):
			items = crypto.decrypt(x=super().get(name='items'))
			items[name] = obj
		else:
			items = {name:obj, '__key__': 'OK'}
		super().put(name='items', obj=crypto.encrypt(x=items))

	def get(self, name):
		if self.locked: self.unlock()
		crypto = Crypto(key=self._key)
		if super().contains(name='items'):
			items = crypto.decrypt(x=super().get(name='items'))
			if name in items:
				return items[name]
			else:
				raise KeyError(f'"{name}" does not exist in the vault!')
		else:
			raise KeyError('vault it empty!')

	def get_all_names(self):
		if self.locked: self.unlock()
		crypto = Crypto(key=self._key)
		if super().contains(name='items'):
			items = crypto.decrypt(x=super().get(name='items'))
			return items.keys()
		else:
			return []

	def remove(self, name):
		if self.locked: self.unlock()
		crypto = Crypto(key=self._key)
		if super().contains(name='items'):
			items = crypto.decrypt(x=super().get(name='items'))
			if name in items:
				del items[name]
				super().put(name='items', obj=crypto.encrypt(x=items))
			else:
				raise KeyError(f'"{name}" does not exist in the vault!')
		else:
			raise KeyError('vault it empty!')

	def contains(self, name):
		if self.locked: self.unlock()
		crypto = Crypto(key=self._key)
		if super().contains(name='items'):
			items = crypto.decrypt(x=super().get(name='items'))
			return name in items
		else:
			return False

	def _check_time(self):
		now = datetime.now()
		if self._key is not None:
			elapsed = now - self._unlock_time
			elapsed_seconds = elapsed.seconds + elapsed.microseconds*1e-6
			if self._timeout is not None:
				if elapsed_seconds>self._timeout:
					print('Timeout!')
					self.lock()

	@property
	def locked(self):
		self._check_time()
		return self._key is None

	def lock(self):
		self.save()
		self._key = None

	_UNLOCK_MESSAGE = 'Please enter the Vault password:'

	def unlock(self, key=None):
		if self._key_type == 'local_id':
			key = get_hardware_uid()

		if key is None:
			print(self._UNLOCK_MESSAGE)
			key = getpass.getpass()
		self._key = key
		# the key might be wrong
		if super().contains(name='items'):
			crypto = Crypto(key=self._key)
			try:
				items = crypto.decrypt(x=super().get(name='items'))
			except ValueError:
				raise ValueError('incorrect key!')
			if items['__key__']!='OK':
				raise ValueError('incorrect key!')

		self._unlock_time = datetime.now()






