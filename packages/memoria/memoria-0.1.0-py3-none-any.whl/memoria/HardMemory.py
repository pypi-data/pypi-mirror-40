from .hash_collection import  make_hash_sha256
from revelio import make_dir, get_path, delete_dir
from .Pickler import Pickler
import os.path
import atexit
from datetime import datetime

# HardMemory is like a dictionary that keeps its objects on the hard drive and does not occupy memory
class HardMemory:
	_ENCODING_BASE = 32

	def __init__(self, path, log_access=True):
		self._path = path
		if os.path.isdir(self._path): self.flush()
		make_dir(path=path)
		atexit.register(self.flush)
		self._log = []
		self._log_access = log_access

	def flush(self):
		if os.path.isdir(self._path):
			delete_dir(self._path)
		else:
			raise ValueError(f'{self._path} is not a directory!')

	def log(self, hash_key, job, text=None):
		self._log.append({'key':hash_key, 'job':job, 'time':datetime.now(), 'text':text})

	@classmethod
	def hash(cls, x):
		return make_hash_sha256(obj=x, base=cls._ENCODING_BASE)

	def save(self, obj, key, text=None, echo=False):
		hash_key = self.hash(x=key)
		Pickler.save(obj=obj, path=get_path(self._path, hash_key))
		job = 'save'
		if echo: print(f'HM {job}:{text} key:{hash_key}')
		if self._log_access: self.log(hash_key=hash_key, job=job, text=text)

	def exists(self, key):
		hash_key = make_hash_sha256(obj=key, base=self._ENCODING_BASE)
		return os.path.isfile(get_path(self._path, hash_key))

	def load(self, key, text=None, echo=False, delete=False):
		hash_key = self.hash(x=key)
		job = 'load'
		result = Pickler.load(path=get_path(self._path, hash_key))
		if self._log_access: self.log(hash_key=hash_key, job=job, text=text)
		if echo: print(f'HM {job}:{text} key:{hash_key}')
		if delete: self.delete(key=key, text=text, echo=echo)
		return result

	def delete(self, key, text=None, echo=False):
		hash_key = self.hash(x=key)
		job = 'delete'
		Pickler.delete(path=get_path(self._path, hash_key))
		if self._log_access: self.log(hash_key=hash_key, job=job, text=text)
		if echo: print(f'HM:{job}-{text}-{hash_key}')

	def __getitem__(self, item):
		return self.load(key=item)

	def __setitem__(self, key, value):
		self.save(obj=value, key=key)