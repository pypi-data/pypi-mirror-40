from setuptools import setup


long_desc = """
akshare
===============
https://github.com/jindaxiang/akshare
Installation
--------------
    pip install akshare

Upgrade
---------------
    pip install akshare --upgrade

"""





setup(
    name='akshare',
    version='0.0.3',
	install_requires = 
		['pandas>=0.23.1',
		'requests>=2.12.4',
		'matplotlib>=2.0.0',
		'lxml',
		'bs4'],
    description='A utility for fundamentals data of OBOR',
	packages = ['akshare'],
	package_data={'': ['*.py','*.json']},
    long_description=long_desc,
    author='Albert King',
    author_email='jindaxiang@163.com',
    url = 'https://github.com/jindaxiang/akshare',
    keywords='OBOR Data'
)

