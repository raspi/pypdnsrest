# -*- encoding: utf8 -*-

import logging
import os
import subprocess
from datetime import datetime

from setuptools import find_packages
from setuptools import setup

log = logging.getLogger(__name__)

here = os.path.abspath(os.path.dirname(__file__))
version_file = os.path.join(here, "VERSION")

__VERSION__ = None

if os.path.isdir(".git"):
    log.debug("Getting version from git.")
    git_timestamp_cmd = ["git", "log", "-1", "--pretty=format:%at"]
    with subprocess.Popen(git_timestamp_cmd, stdout=subprocess.PIPE) as proc:
        proc.wait(10)
        out = proc.stdout.read().strip()
        try:
            d = datetime.fromtimestamp(timestamp=float(int(out)))
            __VERSION__ = "{:%Y.%m.%d.%H%M%S}".format(d)
        except:
            raise ValueError("Couldn't read commit timestamp. Data: '{0}'".format(out))

if __VERSION__ is not None:
    log.debug("Writing version file '{0}'".format(version_file))
    with open(version_file, "w") as f:
        f.write(__VERSION__.strip())

if __VERSION__ is None:
    with open(version_file, "r") as f:
        __VERSION__ = "".join(f.readlines()).strip()

if __VERSION__ is None or __VERSION__ == "":
    raise ValueError("Version file couldn't be loaded.")

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.5",
    "Topic :: Internet :: WWW/HTTP",
    "Operating System :: POSIX :: Linux",
    "Topic :: Software Development :: Libraries",
    "Topic :: System :: Networking",
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
