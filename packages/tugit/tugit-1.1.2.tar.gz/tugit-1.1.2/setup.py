from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='tugit',
	version='1.1.2',
	description='Python library for installing packages directly from a git repository',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/idin/tugit.git',
	author='Idin',
	author_email='d@idin.net',
	license='MIT',
	packages=find_packages(exclude=("jupyter_tests")),
	install_requires=[],
	zip_safe=False
)

