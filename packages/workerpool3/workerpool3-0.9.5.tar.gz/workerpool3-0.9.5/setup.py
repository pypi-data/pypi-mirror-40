#!/usr/bin/python

from setuptools import setup, find_packages

version = '0.9.5'

setup(name='workerpool3',
      version=version,
      description="Module for distributing jobs to a pool of worker threads.",
      long_description="""\
Performing tasks in many threads made fun!

This module facilitates distributing simple operations into jobs that are sent
to worker threads, maintained by a pool object.

It consists of these components:

   1. Jobs, which are single units of work that need to be performed.
   2. Workers, who grab jobs from a queue and perform them.
   3. Worker pool, which keeps track of workers and the job queue.
      """,
      # Strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      ],
      keywords='pooling threading jobs',
      author='Andrey Petrov',
      author_email='andrey.petrov@shazow.net',
      url='https://github.com/shazow/workerpool',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "six"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite='nose.collector'
      )
