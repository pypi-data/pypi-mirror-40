#!/usr/bin/env python

import os
from setuptools import setup

import versioneer


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def get_requirements(filename):
    if not os.path.exists(filename):
        return []

    return parse_requirements(filename)


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]
    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(name='django-mgsub',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Subscribe Mailgun mailing lists from Django',
      long_description=README,
      author='Ferrix Hovi',
      author_email='ferrix+pypi@ferrix.fi',
      install_requires=get_requirements('requirements.txt'),
      tests_require=get_requirements('development.txt'),
      packages=['mgsub'],
      package_data=get_package_data('mgsub'),
      include_package_data=True,
      zip_safe=False,
      url='https://github.com/ferrix/mgsub/',
      license='MIT License',
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 1.8',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      )
