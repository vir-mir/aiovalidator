import os
import re
import sys

from setuptools import setup

install_requires = ['aiohttp>=1.1.6']

PY_VER = sys.version_info

if PY_VER < (3, 4):
    raise RuntimeError("aiovalidator"
                       " doesn't suppport Python earlier than 3.4")


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'aiovalidator', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in '
                               'aiovalidator/__init__.py')


classifiers = [
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Operating System :: POSIX',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Environment :: Web Environment',
    'Development Status :: 4 - Beta',
    'Topic :: Database',
    'Topic :: Database :: Front-Ends',
]


def get_packages(package):
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(name='aiovalidator',
      version=read_version(),
      description='rest, restful validator aiohttp',
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      classifiers=classifiers,
      platforms=['POSIX'],
      author='Alexey Firsov',
      author_email='virmir49@gmail.com',
      url='https://github.com/vir-mir',
      download_url='https://pypi.python.org/pypi/aiovalidator',
      license='Apache-2.0',
      packages=get_packages('aiovalidator'),
      install_requires=install_requires,
      include_package_data=True)
