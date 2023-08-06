#!/usr/bin/env python
import re


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
version = '1.6.9'

if not version:
    raise RuntimeError('Cannot find version information')


with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='wcc',
	author='Jiao Shuai',
	author_email='jiaoshuaihit@gmail.com',
    version=version,
    description='Wikicivi WCC (Wikicivi Crawler Client) SDK',
    long_description=readme,
    packages=['wcc'],
    install_requires=['requests!=2.9.0','oss2','Pillow','tinytag','requests','selenium','imageio'],
    include_package_data=True,
    url='http://wcc.wikicivi.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)

