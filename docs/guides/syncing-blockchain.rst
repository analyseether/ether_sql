Syncing the blockchain
======================

The easiest method to start syncing the sql database to the connected node is using the following command.

.. code:: shell

  $ ether_sql --settings=YourSettings scrape_block_range

The above command picks up node and database settings from :code:`YourSettings`. Then it checks the last block number in sql database and node and start pushing the missing blocks into the database.
To sync blocks in a particular range use the options :code:`--start_block_number` or :code:`--end_block_number` or use the :code:`--help` option to know more about the above command.
options

.. code:: shell

  $ ether_sql scrape_block_range --help

Using multiple workers
----------------------
Syncing the whole blockchain in series would take several months. Hence, to speed up the process we provide options to achieve this task in parallel.
We use RabbitMQ or Redash to maintain the queue of blocks to be pushed in the database.

The following command uses the node, database and queue settings provided in :code:`YourSettings` and starts pushing required blocks in the queue.

.. code :: shell

  $ ether_sql --settings=YourSettings scrape_block_range --mode=parallel

We can then start multiple workers using the following command.

.. code :: shell

  $ ether_sql --settings=YourSettings celery start -c4

The above command will start 4 workers using the provided settings. Here is a demo of the process: https://www.youtube.com/watch?v=rnkfyAgGJwI&feature=youtu.be where we push first 10k blocks in 30 seconds using 10 workers.


Following the block-chain head
------------------------------
A new block gets added in the ethereum blockchain every 15 seconds. It would be very beneficial if we can keep syncing the database with the blockchain in the backend.
This is achieved by running two celery queues, the first queue periodically searches for newly added blocks and pushes them in the second queue, the second queue fetches the block data from the node and pushes it into the database.

The following command starts the periodic queue called :code:`celery_filters`.

.. code :: shell

  $ ether_sql --settings=YourSettings celery start -c1 -B -Q celery_filters

We scan for new blocks every 30 seconds and put all the blocks which are older than :code:`YourSettings.BLOCK_LAG` into the main queue.

The second queue which pushes data into the database can be started using the following command.

.. code :: shell

  $ ether_sql --settings=YourSettings celery start -c4
