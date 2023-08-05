#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name = 'devops_sak',
      version = '1.0.1',
      author = 'Sergio Tocalini Joerg',
      author_email = 'sergiotocalini@gmail.com',
      url = 'https://github.com/sergiotocalini/devops-sak',
      license = 'GNU GPLv3',
      packages = find_packages(),
      classifiers=[
          'Programming Language :: Python',
          ],
      zip_safe=True,
      include_package_data=True,
      entry_points = {
          'console_scripts': [
              'dnsquery = devops_sak.dnsquery:main',
              'lanreporter = devops_sak.lanreporter:main'
          ]
      }
)
