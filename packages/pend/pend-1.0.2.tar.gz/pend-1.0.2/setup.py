#!/usr/bin/env python

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst')) as f:
    long_description = '\n' + f.read()


VERSION = __import__('pend').__version__


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
            rmtree(os.path.join(here, 'build'))
            rmtree(os.path.join(here, 'pend.egg-info'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')
        sys.exit()


setup(
    name='pend',
    version=VERSION,
    description='Pendulum wrapper for short name.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Jo Yongjin',
    author_email='wnrhd114@gmail.com',
    url='https://github.com/joyongjin/pend',
    packages=find_packages(exclude=('tests',)),
    install_requires=['pendulum'],
    license='MIT',
    cmdclass={
        'upload': UploadCommand,
    }
)
