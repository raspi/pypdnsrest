# -*- encoding: utf8 -*-

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

classifiers = [
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP",
]

requires = [
    'requests',
]

entry_points = """
"""

setup(author=u'Pekka Järvinen',
      name='pypdnsrest',
      version='0.1',
      description='PowerDNS REST API',
      long_description='PowerDNS REST API',
      classifiers=classifiers,
      author_email='pekka.jarvinen@gmail.com',
      url='https://github.com/raspi/',
      keywords='dns powerdns pdns rest api web python http',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="pypdnsrest",
      entry_points=entry_points,
      )
