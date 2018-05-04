# ether-sql
Python library to push ethereum blockchain data into an sql database.

# Build Status

ether-sql is written in Python and uses ethjsonrpc for geting data using JSON-RPC calls.

ether-sql was built by Analyse Ether, with the goal of making Ethereum data queryable to everyone. This is currently in very alpha beta, and not recommended for production use until it has received sufficient testing.

It currently supports Parity node but will be expanded to use several nodes.

# Installation guide

1. Install PostgreSQL

`sudo apt-get install postgresql`

2. Create a new user and database
`sudo -u postgres createuser $username --no-superuser --no-createdb --no-createrole`
`sudo -u postgres createdb ether-sql --owner=$username`
