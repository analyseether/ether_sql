# ether_sql
A Python library to push ethereum blockchain data into an sql database.

ether_sql was built by [Analyse Ether](https://www.analyseether.com/), with the goal of making Ethereum data easily available to everyone. This library can be used as a backbone for creating block explorers or performing data analysis.

It is written in Python 3.5+, uses [web3.py](https://github.com/ethereum/web3.py) for geting data using JSON-RPC calls and uses [SqlAlchemy](http://docs.sqlalchemy.org/en/latest/) to connect to a postgressql database.


## Buidl Status
This is currently in very alpha stage, and not recommended for production use until it has received sufficient testing.
Currently supports Geth, Infura and Parity node, but transaction traces (eg. internal transactions) are currently available only with Parity node.

Documentation available at: http://ether-sql.readthedocs.io/en/latest/

# Installation guide

## Linux dependencies

* Install postgresql as database      
`$ sudo apt-get install postgresql`     


## Python dependencies

* Create and activate a virtual environment     
`$ virtualenv envname`     
`$ source envname\bin\activate`

* Install python libraries     
`$ pip install -r requirements.txt`


## Database setup

* Create a new psql user and database     
`$ sudo -u postgres createuser -s -P -e $USER`

This prompts for a user password, use the same password in the settings.py file

* Create the ether_sql database in psql     
`$ createdb ether_sql`

* Create the tables by executing this command from the repo ether_sql       
`$ python ether_sql.py create_tables`

## Node settings
The settings to connect to a node are set in the settings.py file using classes.
* Infura Settings:
The class *PersonalInfuraSettings* specifies settings to connect to a normal Infura node. You can fill in the velue of your API token on NODE_API_TOKEN
```
class PersonalInfuraSettings(DefaultSettings):
    NODE_TYPE = "Infura"
    NODE_API_TOKEN = ""  # your infura api_token
    NODE_URL = 'https://mainnet.infura.io/{}'.format(NODE_API_TOKEN)
```

* Local Node settings
We use the automatic methods in *web3.py* to connect to a node, if a local node is available then only the **NODE_TYPE** is required. The class *PersonalParitySettings* is used to connect to a local Parity node.
```
class PersonalParitySettings(DefaultSettings):
    NODE_TYPE = "Parity"
    # Use this option to parse traces, needs parity with cli --tracing=on
    PARSE_TRACE = True
```

Whereas, the class *PersonalGethSettings* is used to connect to a local Geth node.
```
class PersonalGethSettings(DefaultSettings):
    NODE_TYPE = "Geth"
```

# Syncing data
ether_sql has several built in cli commands to facilitate scraping data. To start the sync just type.
`$ python ether_sql.py --settings='SettingsClassName' scrape_data `

This will start start pushing the data from ethereum node specified in `SettingsClassName` node to the psql database.

To access other helper commands checkout the [docs](http://ether-sql.readthedocs.io/en/latest/api/cli.html).
