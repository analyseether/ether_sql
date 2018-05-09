# ether_sql
A Python library to push ethereum blockchain data into an sql database.

ether_sql was built by [Analyse Ether](https://www.analyseether.com/), with the goal of making Ethereum data easily available to everyone. This library can be used as a backbone for creating block explorers or performing data analysis. 

It is written in Python 2.7, uses [ethjsonrpc](https://github.com/analyseether/ethjsonrpc) for geting data using JSON-RPC calls and uses [SqlAlchemy](http://docs.sqlalchemy.org/en/latest/) to connect to a postgressql database.


## Buidl Status
This is currently in very alpha stage, and not recommended for production use until it has received sufficient testing. 
Currently supports Geth, Infura and Parity node, but transaction traces (eg. internal transactions) are currently available only with Parity node.

# Installation guide

## Linux dependencies

* Install postgresql as database      
`$ sudo apt-get install postgresql`     

* Install pyethereum dependencies     
`$ sudo apt-get install libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev libyaml-cpp-dev`


## Python dependencies

* Create and activate a virtual environment     
`$ virtualenv envname`     
`$ source envname\bin\activate`

* Install python libraries     
`$ pip install -r requirements`


## Database setup

* Create a new psql user and database     
`$ sudo -u postgres createuser -s -P -e $USER`

This prompts for a user password, use the same password in the settings.py file

* Create the ether_sql database in psql     
`$ createdb ether_sql`

* Create the tables by executing this command from the repo ether_sql       
`$ python ether_sql.py create_tables`

## Node settings
Details of connecting to a node are available in the settings.py. Use the settings below for the three supported nodes.

* Infura settings     
```
NODE_TYPE = "Infura"  # Available options 'Geth', 'Parity', 'Infura'
NODE_API_TOKEN = netrc().authenticators('infura.io')[2]  # save the api key in .netrc file with machine name infura.io
NODE_HOST = 'mainnet.infura.io'
NODE_PORT = ""  # no need
```

* Geth settings     
```
NODE_TYPE = "Geth"  # Available options 'Geth', 'Parity', 'Infura'
NODE_API_TOKEN = ""  # no need
NODE_HOST = 'localhost'
NODE_PORT = 8545
```

* Parity settings     
```
NODE_TYPE = "Parity"  # Available options 'Geth', 'Parity', 'Infura'
NODE_API_TOKEN = ""  # no need
NODE_HOST = 'localhost'
NODE_PORT = 8545
```

# Syncing data
ether_sql has several built in cli commands to facilitate scraping data. To start the sync just type     
`$ python ether_sql.py scrape_data `

To access other helper commands try `$ python ether_sql.py` and explore.

