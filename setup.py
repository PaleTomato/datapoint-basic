from setuptools import setup

setup(name='datapoint-basic',
      version='1.0.0',
      description='Simple access to Met Office\s datapoint API',
      url='https://github.com/PaleTomato/datapoint-basic',
      author='Patrick Leedham',
      author_email='ptl76@hotmail.co.uk',
      license='GPL-3.0',
      packages=['datapointbasic'],
      install_requires=[
          'datapoint'
      ])