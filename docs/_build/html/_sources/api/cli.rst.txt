Command Line Interface (CLI)
============================

ether_sql has several built in CLI commands to interact with the node and sql table. This section aims at detailing the various cli options available in the library in detail.

We use the `Click <http://click.pocoo.org/5/>`_ library to generate CLI groups and their nested commands in a tree structure.


Group --> ether_sql.py
----------------------
:code:`python ether_sql.py` is the most basic CLI group with 4 subsequent commands.

.. code-block:: shell

  $ python ether_sql.py
  Usage: ether_sql.py [OPTIONS] COMMAND [ARGS]...

    CLI script for ether_sql

    Options:
      --help  Show this message and exit.

    Commands:
      check_settings  Show the settings as ether_sql sees them...
      ether           Manages the ether node (query the node).
      scrape_data     Pushes the data between sql_block_number and...
      sql             Manages the sql (create/drop/query tables).


Command --> ether_sql.py scrape_data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:code:`python ether_sql.py scrape_data` command starts pushing the blocks from ether node to sql. If no option is provided it automatically checks for the last block_number in sql and starts sync from that block.

.. code-block:: shell

  $ python ether_sql.py scrape_data --help
  Usage: ether_sql.py scrape_data [OPTIONS]

  Pushes the data between sql_block_number and node_block_number in the database

  Options:
    --sql_block_number TEXT   block number in sql
    --node_block_number TEXT  block number in node
    --help                    Show this message and exit.


Group --> ether_sql.py ether
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:code:`python ether_sql.py ether` is a group which contains commands to interact with the ethereum node.


.. code-block:: shell

  $ python ether_sql.py ether
  Usage: ether_sql.py ether [OPTIONS] COMMAND [ARGS]...

  Manages the ether node (query the node).

  Options:
    --help  Show this message and exit.

  Commands:
    eth_blocknumber  Gives the most recent block number in the...


Group --> ether_sql.py sql
^^^^^^^^^^^^^^^^^^^^^^^^^^
:code:`python ether_sql.py sql` is a group which contains commands to interact with the sql database.

.. code-block:: shell

  $ python ether_sql.py sql
  Usage: ether_sql.py sql [OPTIONS] COMMAND [ARGS]...

  Manages the sql (create/drop/query tables).

  Options:
    --help  Show this message and exit.

  Commands:
    create_tables    Create the database tables.
    drop_tables      Drop the database tables.
    sql_blocknumber  Gives the current highest block in database
