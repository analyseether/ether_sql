Quickstart
==========
This quickstart is a follow up the `Installation <../installation>`_ instructions.

Syncing the blockchain
----------------------

The easiest method to start syncing the sql database to the connected node is using the following command.

.. code:: shell

  $ python ether_sql.py scrape_data

This command will check the last block number in your sql database and node and start pushing the remaining blocks into your sql server.
To sync blocks in a particular range use the options :code:`--sql_block_number` or :code:`--node_block_number` or use the :code:`--help` option to know more about the above command.

To get the current status of sync progress you can use the following command to get the highest block number in the sql.

.. code:: shell

  $ python ether_sql.py sql sql_blocknumber

For more detail refer to the API doc on `CLI's <../api/cli>`_.

Connecting to Postgresql
------------------------
Once the database is filled with some blocks you can connect to the psql database using the following command.

.. code:: shell

  $ psql ether_sql

Once connected to the Postgresql you can start quickly querying the database.
Below is a simple code to get the maximum block number in the sql database.

.. code:: sql

  ether_sql=# SELECT max(block_number) from blocks;
