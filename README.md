# ether-sql
Python library to push ethereum blockchain data into an sql database.

# Build Status

ether-sql is written in Python and uses ethjsonrpc for geting data using JSON-RPC calls.

ether-sql was built by Analyse Ether, with the goal of making Ethereum data queryable to everyone. This is currently in very alpha beta, and not recommended for production use until it has received sufficient testing.

It currently supports Parity node but will be expanded to use several nodes.

# Installation guide

1. Install PostgreSQL

`sudo apt-get install postgresql`

2. Create a new psql user and database

`sudo -u postgres createuser -s -P -e $USER`

This prompts for a user password, use the same password in the settings.py file

`createdb ether-sql`
