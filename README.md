# ether_sql
A Python library to push ethereum blockchain data into an sql database.

ether_sql was built by [Analyse Ether](https://www.analyseether.com/), with the goal of making Ethereum data easily available to everyone. This library can be used as a backbone for creating block explorers or performing data analysis.

It is written in Python 3.5+, uses [web3.py](https://github.com/ethereum/web3.py) for geting data using JSON-RPC calls and uses [SqlAlchemy](http://docs.sqlalchemy.org/en/latest/) to connect to a postgressql database.


## Buidl Status
This is currently in very alpha stage, and not recommended for production use until it has received sufficient testing.
Currently supports Geth, Infura and Parity node, but transaction traces (eg. internal transactions) are currently available only with Parity node.

[![Build Status](https://travis-ci.org/analyseether/ether_sql.svg?branch=master)](https://travis-ci.org/analyseether/ether_sql)

Documentation available at: http://ether-sql.readthedocs.io

# Installation guide

Please find the detailed installation guide [here](http://ether-sql.readthedocs.io/en/latest/installation.html)


# Command line options
ether_sql has several built in cli commands to facilitate scraping data.

## Syncing the data
To start the sync just type.


`$ ether_sql scrape_block_range `

This will start start pushing the data from an Infura node to the psql database.


## Switching nodes

To switch nodes use the settings flag:


`$ ether_sql --settings='PersonalParitySettings' scrape_block_range `


## Using multiple workers to sync data
To start 4 parallel workers use.

`$ ether_sql --settings=YourSettings celery start -c4`

The above command will start 4 workers using the settings `YourSettings`
Then start the sync, which will automatically use the setting used to start workers.
`$ ether_sql scrape_block_range `

Here is a demo of the process: https://www.youtube.com/watch?v=rnkfyAgGJwI&feature=youtu.be 

## Exporting as csv

To export the pushed data as a csv

`$ ether_sql sql export_to_csv`


To access other Command Line Interfaces (CLI) checkout the [cli docs](http://ether-sql.readthedocs.io/en/latest/api/cli.html).
