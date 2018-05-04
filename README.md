# ether-sql
Python library to push ethereum blockchain data into an sql database.

# Build Status

ether_sql is written in Python 2.7, uses [ethjsonrpc](https://github.com/analyseether/ethjsonrpc) for geting data using JSON-RPC calls and uses SqlAlchemy to connect to postgressql database.

ether_sql was built by Analyse Ether, with the goal of making Ethereum data
easily to everyone. This library can be used as a backbone for creating block explorers or as a backbone for data analysis needs. This is currently in very alpha beta, and not recommended for production use until it has received sufficient testing.

It currently supports Parity node but will be expanded to use several nodes.

# Installation guide

1. Install PostgreSQL

`sudo apt-get install postgresql`

2. Create a new psql user and database

`sudo -u postgres createuser -s -P -e $USER`

This prompts for a user password, use the same password in the settings.py file

`createdb ether_sql`
