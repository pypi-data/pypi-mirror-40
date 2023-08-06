import dill
import pickle
import send2trash
from pathlib import Path
import os

class Pickler:
	@staticmethod
	def save(path, obj, method='dill', echo=0):
		echo = max(0, echo)
		temp_path = path+'.temp'

		with open(file=temp_path, mode='wb') as output:

			if method == 'dill':
				try:
					dill.dump(obj=obj, file=output, protocol=dill.HIGHEST_PROTOCOL)
					successful_method = 'dill'
					if echo>1: print(f'dilled {temp_path}')
				except:
					pickle.dump(obj=obj, file=output, protocol=pickle.HIGHEST_PROTOCOL)
					successful_method = 'pickle'
					if echo>1: print(f'pickled {temp_path}')
			else:
				try:
					pickle.dump(obj=obj, file=output, protocol=pickle.HIGHEST_PROTOCOL)
					successful_method = 'pickle'
					if echo>1: print(f'pickled {temp_path}')
				except:
					dill.dump(obj=obj, file=output, protocol=dill.HIGHEST_PROTOCOL)
					successful_method = 'dill'
					if echo>1: print(f'dilled {temp_path}')
		if Pickler.file_exists(path=path):
			Pickler.delete(path=path)
		os.rename(temp_path, path)
		if echo:
			additional_message = '' if successful_method == method else f' because {method} failed!'
			if successful_method == 'dill':
				print(f'dilled "{path}"'+additional_message)
			else:
				print(f'pickled "{path}"'+additional_message)



	write = save
	put = save
	dump = save
	pickle = save

	@staticmethod
	def file_exists(path):
		return Path(path).is_file()

	@staticmethod
	def load(path, method='dill', echo=0):
		echo = max(0, echo)
		with open(file=path, mode='rb') as input:

			if method == 'dill':
				try:
					obj = dill.load(file=input)
					if echo: print(f'undilled {path}')
				except:
					obj = pickle.load(file=input)
					if echo: print(f'unpickled {path}')
			else:
				try:
					obj = pickle.load(file=input)
					if echo: print(f'unpickled {path}')
				except:
					obj = dill.load(file=input)
					if echo: print(f'undilled {path}')
		return obj

	read = load
	get = load

	@classmethod
	def delete(cls, path):
		if cls.file_exists(path=path):
			send2trash.send2trash(path)
		else:
			raise FileNotFoundError(f'"{path}" not found!')
		if cls.file_exists(path=path):
			backup_path = path + '.deleted'
			if cls.file_exists(backup_path):
				os.remove(backup_path)
			os.rename(path, backup_path)
