# -*- encoding: utf8 -*-

import logging
import os
import sys
import subprocess
from datetime import datetime

from setuptools import find_packages, setup

log = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s',
    stream=sys.stdout,
    level=logging.INFO,
)

# Package metadata.
LICENSE = 'Apache 2.0'
NAME = 'pypdnsrest'
URL = 'https://github.com/raspi/pypdnsrest'
AUTHOR = u'Pekka Järvinen'
EMAIL = 'pekka.jarvinen@gmail.com'
DESCRIPTION = 'PowerDNS REST API Client'
LONG_DESCRIPTION = """PowerDNS REST API Client for Python 3.x"""

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.5",
    "Topic :: Internet :: WWW/HTTP",
    "Operating System :: POSIX :: Linux",
    "Topic :: Software Development :: Libraries",
    "Topic :: System :: Networking",
]

KEYWORDS = 'dns powerdns pdns rest api web python http'

REQUIRES = [
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


# End of metadata

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
            __VERSION__ = "{:%Y.%-m.%-d.%-H%M%S}".format(d)
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

setup(author=AUTHOR,
      name=NAME,
      version=__VERSION__,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      classifiers=CLASSIFIERS,
      author_email=EMAIL,
      url=URL,
      license=LICENSE,
      keywords=KEYWORDS,
      packages=find_packages(),
      include_package_data=False,
      zip_safe=False,
      install_requires=REQUIRES,
      extras_require={
          'testing': testing_extras,
      },
      tests_require=tests_require,
      test_suite="{0}.tests".format(NAME),
      entry_points=entry_points,
      )
