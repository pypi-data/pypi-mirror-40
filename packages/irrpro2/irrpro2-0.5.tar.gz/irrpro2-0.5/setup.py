from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='irrpro2',
      version='0.5',
      author='Dmitriy Proshkin',
      author_email='dmitriyproshkin@gmail.com',
      license='MIT',
      packages=['irrpro2'],
      install_requires=[
      		'numpy',
      		'lxml',
      		'requests',
      ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)