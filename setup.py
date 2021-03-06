#!/usr/bin/python

from setuptools import setup, find_packages, Command
import os.path, sys
import re

_here = os.path.abspath(os.path.dirname(__file__))

def version():
    # This rather complicated mechanism is employed to avoid importing any
    # yet unfulfilled dependencies, for instance when installing under
    # Python 2.4 from scratch
    import imp
    path = os.path.join(_here, 'amazonproduct', 'version.py')
    mod = imp.load_source('version', path)
    return mod.VERSION

def read(fname):
    try:
        # makes sure that setup can be executed from a different location
        return open(os.path.join(_here, fname)).read()
    except IOError:
        return ''

def readme():
    # substitute all include statements.
    def insert_include(matchobj):
        return read(matchobj.group(1))
    return re.sub(r'\.\. include:: (\w+)', insert_include, read('README'))

class PyTest(Command):
    """
    setuptools/distutils command to run py.test.
    """
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass
    def run(self):
        import subprocess
        errno = subprocess.call([
            sys.executable, os.path.join(_here, 'tests', 'runtests.py'), '-vl'])
        raise SystemExit(errno)

# make sure that no development version end up on PyPI
if 'register' in sys.argv or 'upload' in sys.argv:
    version_ = version()
    if '/' in version_ or '+' in version_:
        print('ERROR: Version %r has not been adjusted yet!' % version_)
        sys.exit(1)

setup(
    name='python-amazon-product-api',
    version=version(),
    author='Sebastian Rahlf',
    author_email='basti AT redtoad DOT de',
    url="http://bitbucket.org/basti/python-amazon-product-api/downloads/",
    license='bsd',

    description='A Python wrapper for the Amazon Product Advertising API.',
    long_description=readme(),
    zip_safe=False,  # we want to find README.rst and version.py
    keywords='amazon product advertising api wrapper signed requests',

    packages=find_packages(_here, exclude=['tests']),

    cmdclass={'test': PyTest},
    install_requires=['requests'],
    tests_require=[
        'pytest-localserver>=0.3',
        'lxml',
        'six',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python', 
        'Programming Language :: Python :: 2.6', 
        'Programming Language :: Python :: 2.7', 
        'Programming Language :: Python :: 3.3', 
    ],
)
