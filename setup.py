#!/usr/bin/env python
import os
import sys
import codecs
from setuptools import setup, find_packages

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(ROOT)
from page_exporter import NAME, get_version
reqs = 'install.py%d.pip' % sys.version_info[0]

def read(*files):
    content = ''
    for f in files:
        content += codecs.open(os.path.join(ROOT, 'requirements', f), 'r').read()
    return content


install_requires = read('install.any.pip', reqs),
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
    install_requires=install_requires,
    extras_require={
        'test': tests_require,
        'dev': dev_require + tests_require,
    },
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
    ]
)
