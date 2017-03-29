#!/usr/bin/env python
import os
import sys
import codecs
from distutils.config import PyPIRCCommand
from setuptools import setup, find_packages

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(ROOT)
from page_exporter import NAME, get_version

def read(*files):
    content = ''
    for f in files:
        content += codecs.open(os.path.join(ROOT, 'requirements', f), 'r').read()
    return content


dev_require = read('develop.pip')
tests_require = read('testing.pip')

setup(
    name=NAME,
    version=get_version(),
    url='https://github.com/marcoimme/%s/' % NAME,

    author='Marco Immediato',
    author_email='marcoimme@gmail.com',
    license="MIT",
    description='Django Page Exporter',

    package_dir={'': 'src'},
    packages=find_packages(where=ROOT),

    include_package_data=True,
    install_requires=read('install.pip'),
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
    ]
)
