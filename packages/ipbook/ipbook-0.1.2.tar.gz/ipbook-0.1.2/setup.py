from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
	name='ipbook',
	version='0.1.2',
	description='Allows you to save IP addresses so that they are accessible in the command line',
	author='Brandon J. Yi',
	author_email='bypie966@gmail.com',
	packages=['ipbook'],
	entry_points = {
		'console_scripts': [
			'ipbook = ipbook.__main__:main'
		]
	},
	include_package_data=True,
	long_description=long_description,
    long_description_content_type="text/markdown"
)
