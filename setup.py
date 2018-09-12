#!/usr/bin/env python

from distutils.core import setup

setup(name='py-socket-server',
      version='0.1',
      description='Framework for a Unix Domain Socket based daemon application',
      author='Stefan Wolfsheimer',
      author_email='s.wolfsheimer@surfsara.nl',
      packages=['socket_server'],
      install_requires=[])
