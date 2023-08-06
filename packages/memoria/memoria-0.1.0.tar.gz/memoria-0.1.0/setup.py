from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='memoria',
	version='0.1.0',
	description='Python library for saving memory, encryption, and password management',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/idin/memoria',
	author='Idin',
	author_email='d@idin.net',
	license='',
	packages=find_packages(exclude=("jupyter_tests", ".idea", ".git")),
	install_requires=['send2trash', 'pathlib', 'base32hex', 'datetime', 'aenum', 'dill', 'uuid'],
	python_requires='~=3.5',
	zip_safe=False
)