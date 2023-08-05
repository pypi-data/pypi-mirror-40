py-stellar-base
===============


Python libraries that allow you to interface with the stellar.org horizon interface. Stellar-base library consists of classes to read, write, hash, and sign the xdr structures that are used in stellar-core.


# install
    pip install stellar-base

# requirements
    ed25519 requires python-dev to be installed
    ubuntu/debian:
    sudo apt-get install python-dev  # for python2.x installs
    sudo apt-get install python3-dev  # for python3.x installs
    yum:
    sudo yum install python-devel
    
check out full stellar development docs at:
https://www.stellar.org/developers/guides/

And the laboratory:
https://www.stellar.org/laboratory/#?network=test

#getting lumens
    The Stellar blockchain functions with lumens for settlement and account creation.
    To get some lumens (xlm)

    Test network:
    url = 'https://horizon-testnet.stellar.org'
    r = requests.get(url + '/friendbot?addr=' + kp.address().decode('ascii')) # Get 1000 lumens
    Live:
    https://binance.com
    https://tempo.eu.com
    https://btc38.com


.. image:: https://img.shields.io/travis/StellarCN/py-stellar-base.svg?style=flat-square&maxAge=1800
    :alt: Travis (.org)
    :target: https://travis-ci.org/StellarCN/py-stellar-base/

.. image:: https://img.shields.io/readthedocs/stellar-base.svg?style=flat-square&maxAge=1800
    :alt: Read the Docs
    :target: https://stellar-base.readthedocs.io/en/latest/

.. image:: https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base.svg?style=flat-square&maxAge=1800
    :alt: Codecov
    :target: https://codecov.io/gh/StellarCN/py-stellar-base


It provides:

- a networking layer API for Horizon endpoints.
- facilities for building and signing transactions, for communicating with a Stellar Horizon instance, and for submitting transactions or querying network history.
- you can use stellar.org's version of Horizon or setup your own node to query and submit transactions
- I review all code submitted onto pypi manually
- the maintainer email address is maintained with 2 factor hardware authentication and the pypi account password is 18 random characters.

Installing
----------

Install from pypi, there are two packages here, please choose one of them:


* The current conservative package is maintained by antb123. |stellar-base-image|

.. |stellar-base-image| image:: https://img.shields.io/pypi/v/stellar-base.svg?style=flat-square&maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-base

.. code-block:: text

    pip install -U stellar-base

* The package is built automatically by Travis-CI. |stellar-sdk-image|

.. |stellar-sdk-image| image:: https://img.shields.io/pypi/v/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-sdk

.. code-block:: text

    pip install -U stellar-sdk


Install from latest source code(*may be unstable*):

.. code-block:: text

    pip install git+git://github.com/StellarCN/py-stellar-base


A Simple Example
----------------

.. code-block:: python

    # Alice pay 10.25 XLM to Bob
    from stellar_base.builder import Builder

    alice_secret = 'SCB6JIZUC3RDHLRGFRTISOUYATKEE63EP7MCHNZNXQMQGZSLZ5CNRTKK'
    bob_address = 'GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH'

    builder = Builder(secret=alice_secret)
    builder.add_text_memo("Hello, Stellar!").append_payment_op(
        destination=bob_address, amount='10.25', asset_code='XLM')
    builder.sign()
    response = builder.submit()
    print(response)


Document
--------
* Quick Start: https://stellar-base.readthedocs.io/en/latest/quickstart.html
* API: https://stellar-base.readthedocs.io/en/latest/api.html
* XDR:  https://en.wikipedia.org/wiki/External_Data_Representation


Links
-----
* Examples: https://github.com/StellarCN/py-stellar-base/tree/master/examples
* Releases: https://pypi.org/project/stellar-base/
* Code: https://github.com/StellarCN/py-stellar-base
* Issue tracker: https://github.com/StellarCN/py-stellar-base/issues
* License Apache License 2.0: https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE

Thank you to all the people who have already contributed to py-stellar-base!

