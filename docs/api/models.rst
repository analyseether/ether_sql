SQL Tables
==========

This section aims at giving a detailed description of the psql tables in the database and their corresponding helper functions.

.. figure:: ../_static/ethereum_state_machine.jpeg
   :scale: 80 %



Blocks
------
As visible from the image above, a blockchain is literally a chain of blocks. A block contains a list of transactions, few features to prove the work done by a miner and a list of uncles.

.. autoclass:: ether_sql.models.blocks.Blocks

Transactions
------------
A transaction is the basic method for Ethereum accounts to interact with each other. The transaction is a single cryptographically signed instruction sent to the Ethereum network and has the capacity to change the world state.

.. autoclass:: ether_sql.models.transactions.Transactions

Uncles
------
Due to ethereum block-chains fast block propagation time (~15 seconds), the probability of a block with sufficient proof-of-work becoming stale becomes quite high. This reduces the security and miner decentralization of block-chain. To rectify this issue ethereum proposes a modified-GHOST protocol by including and rewarding uncles (ommers) or stale blocks not included in the blockchain.

.. autoclass:: ether_sql.models.uncles.Uncles

Receipts
--------
Receipts information concerning the execution of a transaction in the block-chain. They can be useful to form a zero-knowledge proof, index and search, and debug transactions. The status column was included after the Byzantinium hardfork.

.. autoclass:: ether_sql.models.receipts.Receipts

Logs
----
The logs table contains the logs which were accrued during the execution of the the transaction, they are helpful in deciphering smart-contract executions or message calls.

.. autoclass:: ether_sql.models.logs.Logs

Traces
------
The trace module is for getting a deeper insight into transaction processing, can be used to debugging transactions and also access the internal transactions which are not included in a block.

.. autoclass:: ether_sql.models.traces.Traces

StateDiff
---------

The state diff table contains information about the change in state after each transaction or block

.. autoclass:: ether_sql.models.state_diff.StateDiff

StorageDiff
-----------

The storage diff table contains information about the change in storage after each contract execution

.. autoclass:: ether_sql.models.storage_diff.StorageDiff
