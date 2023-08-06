from .encrypt import encrypt as _encrypt
from .encrypt import decrypt as _decrypt
import dill as pickle

class Crypto:
	# Crypto is a class that can encrypt or decrypt an object
	def __init__(self, key):
		self._key = str(key)

	def encrypt(self, x):
		clear = pickle.dumps(x, protocol=0)
		clear = clear.decode(encoding='utf-8')
		return _encrypt(key=self._key, clear=clear)

	def decrypt(self, x):
		clear_string = _decrypt(key=self._key, encrypted=x)
		return pickle.loads(clear_string.encode(encoding='utf-8'))

	def write_pickle(self, x, file):
		encrypted = self.encrypt(x)
		pickle.dump(obj=encrypted, file=open(file=file, mode='wb'))

	def read_pickle(self, file):
		encrypted = pickle.load(file=open(file=file, mode='rb'))
		return self.decrypt(encrypted)