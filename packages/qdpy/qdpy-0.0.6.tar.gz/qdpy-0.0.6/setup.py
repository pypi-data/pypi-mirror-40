#!/usr/bin/env python3


from setuptools import setup, find_packages
import qdpy

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

packages = find_packages(exclude=['examples'])

setup(name='qdpy',
      version=qdpy.__version__,
      description='Quality-Diversity algorithms in Python',
      url='https://gitlab.com/leo.cazenille/qdpy',
      author='Leo Cazenille',
      author_email='leo.cazenille@gmail.com',
      license='LGPLv3',
      packages=packages,
      install_requires=requirements,
      zip_safe=False)

# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
