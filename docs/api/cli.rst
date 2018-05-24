Command Line Interface (CLI)
============================

ether_sql has several built in CLI commands to interact with the node and sql table. This section aims at detailing the various cli options available in the library in detail.

We use the `Click <http://click.pocoo.org/5/>`_ library to generate CLI groups and their nested commands in a tree structure.

Group: ether_sql
----------------

.. click:: ether_sql.cli:cli
  :prog: ether_sql

SubGroup: ether_sql ether
^^^^^^^^^^^^^^^^^^^^^^^^^

.. click:: ether_sql.cli.ether:ether
  :prog: ether_sql ether
  :show-nested:

SubGroup: ether_sql sql
^^^^^^^^^^^^^^^^^^^^^^^

.. click:: ether_sql.cli.sql:sql
  :prog: ether_sql sql
  :show-nested:

Command: ether_sql scrape_block_range
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. click:: ether_sql.cli:scrape_block_range
  :prog: ether_sql scrape_block_range

Command: ether_sql scrape_block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. click:: ether_sql.cli:scrape_block
  :prog: ether_sql scrape_block
