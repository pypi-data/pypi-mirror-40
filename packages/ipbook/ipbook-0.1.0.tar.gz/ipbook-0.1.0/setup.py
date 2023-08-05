from setuptools import setup, find_packages

setup(
	name='ipbook',
	version='0.1.0',
	description='Like a contacts app, but for your personal list of IP addresses',
	author='Brandon J. Yi',
	packages=['ipbook'],
	entry_points = {
		'console_scripts': [
			'ipbook = ipbook.__main__:main'
		]
	},
	include_package_data=True
)
