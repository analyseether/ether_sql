Installation Guide
==================

Linux dependencies
------------------

Install postgresql as database:

.. code:: sh
    $ sudo apt-get install postgresql

Install pyethereum dependencies

.. code:: sh
    $ sudo apt-get install libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev libyaml-cpp-dev


Python dependencies
-------------------

Create and activate a virtual environment

.. code:: sh
    $ virtualenv envname
    $ source envname\bin\activate

Install python libraries

.. code:: sh
    $ pip install -r requirements


Database setup
--------------

Create a new psql user and database. This prompts for a user password, use the same password in the variable **SQLALCHEMY_PASSWORD** of the settings.py file

.. code:: sh
    $ sudo -u postgres createuser -s -P -e $USER



Create the ether_sql database in psql

.. code:: sh
    $ createdb ether_sql

Create the tables by executing this command from the repo ether_sql

.. code:: sh
    $ python ether_sql.py create_tables`

Node settings
-------------

Details of connecting to a node are available in the settings.py. Use the settings below for the three supported nodes.

Infura settings

.. code:: python
    NODE_TYPE = "Infura"  # Available options 'Geth', 'Parity', 'Infura'
    NODE_API_TOKEN = netrc().authenticators('infura.io')[2]  # save the api key in .netrc file with machine name infura.io
    NODE_HOST = 'mainnet.infura.io'
    NODE_PORT = ""  # no need


Geth settings

.. code:: python
  NODE_TYPE = "Geth"  # Available options 'Geth', 'Parity', 'Infura'
  NODE_API_TOKEN = ""  # no need
  NODE_HOST = 'localhost'
  NODE_PORT = 8545


Parity settings

.. code:: python
  NODE_TYPE = "Parity"  # Available options 'Geth', 'Parity', 'Infura'
  NODE_API_TOKEN = ""  # no need
  NODE_HOST = 'localhost'
  NODE_PORT = 8545
