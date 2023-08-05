# coding: utf-8

from distutils.core import setup
from setuptools import setup, find_packages
import codecs

import os
long_description = 'stellar-base is used for accessing the stellar.org blockchain with python using the horizon backend'
if os.path.exists('README.rst'):
    with codecs.open('README.rst', encoding='utf-8') as file:
        long_description = file.read()


setup(
    name = 'stellar-base',
    version = '1.0.1.2',
    description = """Conservative Version of library for managing Stellar.org blockchain transactions and accounts 
    using stellar-base in python. Allows full functionality interfacing
    with the Horizon front end. Code is audited. See https://www.stellar.org/developers/ for more info""",
    url = 'http://github.com/stellarCN/py-stellar-base/',
    license = 'Apache',
    maintainer='antb123',
    maintainer_email='awbarker@gmail.com',
    author = 'eno, overcat',
    author_email = 'appweb.cn@gmail.com',
    include_package_data = True,
    packages=find_packages(),
    long_description = long_description,
    keywords=['stellar.org','lumens','xlm','blockchain', "distributed exchange", "cryptocurrency", "dex",
              "stellar-core", "horizon", "sdex", "trading", "Stellar"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'ed25519', 'crc16', 'requests', 'SSEClient', 'numpy'
    ]
)
