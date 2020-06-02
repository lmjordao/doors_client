from setuptools import setup

setup(name='doors-client',
      version='0.1.0',
      packages=['app'],
      entry_points={
          'console_scripts': [
              'doors-client = api.__main__:main'
          ]
      }, install_requires=['requests']
      )
