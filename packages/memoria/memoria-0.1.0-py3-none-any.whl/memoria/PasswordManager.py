from .Vault import Vault
import getpass

class PasswordManager(Vault):
	def __init__(self, path, key=None, extension='memp'):
		super().__init__(path=path, key=key, timeout=None, extension=extension)

	_UNLOCK_MESSAGE = 'Please enter the Password Manager key:'

	def get_password(self, key):
		if self.contains(name=key):
			return self.get(name=key)
		else:
			print(f'You have not entered the password for {key}. Please enter it:')
			password = getpass.getpass()
			self.put(name=key, obj=password)
			return password

	def __getitem__(self, key):
		return self.get_password(key=key)

	def put(self, name, obj):
		super().put(name=name, obj=obj)
		self.save(echo=False)

	def update_password(self, x):
		password = getpass.getpass()
		self.put(name=x, obj=password)


