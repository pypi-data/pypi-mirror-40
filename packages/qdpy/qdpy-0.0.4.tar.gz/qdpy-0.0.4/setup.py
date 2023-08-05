#!/usr/bin/env python3


from setuptools import setup, find_packages
import qdpy

packages = find_packages(exclude=['examples'])

setup(name='qdpy',
      version=qdpy.__version__,
      description='Quality-Diversity algorithms in Python',
      url='https://gitlab.com/leo.cazenille/qdpy',
      author='Leo Cazenille',
      author_email='leo.cazenille@gmail.com',
      license='LGPLv3',
      packages=packages,
      install_requires=['numpy', 'scipy', 'sklearn', 'matplotlib'],
      zip_safe=False)

# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
