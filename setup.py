# -*- encoding: utf8 -*-

import os
import subprocess
from datetime import datetime

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

__VERSION__ = None

git_timestamp_cmd = ["git", "log", "-1", "--pretty=format:%at"]
with subprocess.Popen(git_timestamp_cmd, stdout=subprocess.PIPE) as proc:
    proc.wait(10)
    out = proc.stdout.read().strip()
    try:
        d = datetime.fromtimestamp(timestamp=float(int(out)))
        __VERSION__ = "{:%Y.%m.%d.%H%M%S}".format(d)
    except:
        raise ValueError("Couldn't read commit timestamp. Data: '{0}'".format(out))

if __VERSION__ is None:
    raise ValueError("Version is None.")

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP",
]

requires = [
    'requests',
]

entry_points = """
"""

tests_require = [
]

testing_extras = tests_require + [
    'nose',
    'coverage',
    'virtualenv',
]

setup(author=u'Pekka Järvinen',
      name='pypdnsrest',
      version=__VERSION__,
      description='PowerDNS REST API',
      long_description='PowerDNS REST API',
      classifiers=classifiers,
      author_email='pekka.jarvinen@gmail.com',
      url='https://github.com/raspi/pypdnsrest',
      license='Apache 2.0',
      keywords='dns powerdns pdns rest api web python http',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={
          'testing': testing_extras,
      },
      tests_require=tests_require,
      test_suite="pypdnsrest.tests",
      entry_points=entry_points,
      )
