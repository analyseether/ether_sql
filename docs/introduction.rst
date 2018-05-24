Introduction
============

ether_sql
~~~~~~~~~~~~~~~~

ether_sql is a Python library to push ethereum blockchain data into an sql database.

It is maintained by `Analyse Ether <https://www.analyseether.com/>`_, with the goal of making Ethereum data easily available to everyone. This library can be used as a backbone for creating block explorers or performing data analysis.

It is written in Python 3.5+, uses `web3.py <https://github.com/ethereum/web3.py>`_ for geting data using JSON-RPC calls and uses `SqlAlchemy <http://docs.sqlalchemy.org/en/latest/>`_ to connect to a postgressql database.

Goals
-----

The main focus is to make Ethereum data easily available to everyone, while serving as a backbone for:

* Open block explorers (coming soon...)
* `Data analysis platforms <https://www.analyseether.com/>`_

Buidl Status
------------
This is currently in very alpha stage, and not recommended for production use until it has received sufficient testing.
Currently supports Geth, Infura and Parity node, but transaction traces (eg. internal transactions) are currently available only with Parity node.


Follow along the `Installation <installation.html>`_ to install the basic setup and checkout the `Guides <./guides/index.html>`_ to understand the process.
