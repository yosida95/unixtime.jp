# -*- coding: utf-8 -*-

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
requires = []
tests_require = []


def read(name):
    try:
        with open(os.path.join(here, name)) as fd:
            return fd.read()
    except:
        return ""

README = read('README.rst')

setup(name='unixtimejp',
      version='0.0',
      description='http://unixtime.jp/',
      author='Kohei YOSHIDA',
      author_email='kohei.yoshida@gehirn.co.jp',
      long_description=README,
      url='https://github.com/yosida95/unixtime.jp',
      py_modules=['unixtimejp'],
      install_requires=requires,
      tests_require=tests_require,
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ])
