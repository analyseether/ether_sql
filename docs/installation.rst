Installation Guide
==================

Linux dependencies
------------------

Install postgresql as database::

  $ sudo apt-get install postgresql


Python dependencies
-------------------
Clone the **ether_sql** library::

  $ git clone https://github.com/analyseether/ether_sql.git
  $ cd ether_sql

Create and activate a virtual environment::

  $ virtualenv envname
  $ source envname\bin\activate

Install python libraries::

  $ pip install -e . -r requirements.txt


Database setup
--------------

Create a new psql user, this prompts for a user password, use the same password in the variable :code:`SQLALCHEMY_PASSWORD` of the **settings.py** file::

  $ sudo -u postgres createuser -s -P -e $USER


Create the ether_sql database in psql::

    $ createdb ether_sql

Create the tables by executing this command from the repo ether_sql::

    $ ether_sql create_tables

Node settings
-------------
The settings to connect to a node are set in the **settings.py** file using classes.

Infura Settings:
^^^^^^^^^^^^^^^^

The class **PersonalInfuraSettings** specifies settings to connect to a normal Infura node. You can fill in the value of your API token on **NODE_API_TOKEN**::

  class PersonalInfuraSettings(DefaultSettings):
      NODE_TYPE = "Infura"
      NODE_API_TOKEN = ""  # your infura api_token
      NODE_URL = 'https://mainnet.infura.io/{}'.format(NODE_API_TOKEN)

Local Node settings:
^^^^^^^^^^^^^^^^^^^^

We use the automatic methods in **web3.py** to connect to a node, if a local node is available then only the **NODE_TYPE** is required. The class **PersonalParitySettings** is used to connect to a local Parity node::

  class PersonalParitySettings(DefaultSettings):
      NODE_TYPE = "Parity"
      # Use this option to parse traces, needs parity with cli --tracing=on
      PARSE_TRACE = True


Whereas, the class **PersonalGethSettings**  is used to connect to a local Geth node::

  class PersonalGethSettings(DefaultSettings):
      NODE_TYPE = "Geth"


Syncing data
------------

ether_sql has several built in cli commands to facilitate scraping data. To start the sync just type::

  $ ether_sql scrape_data

This will by default start pushing the data from an Infura node to the psql database. To switch nodes use the settings flag::

  $ ether_sql --settings='PersonalParitySettings' scrape_data


To access other Command Line Interfaces (CLI) checkout the `CLI's <./api/cli.html>`_.
