SQL Examples
============

This is a list of some basic SQL queries written with the synced database. This page is a follow up on the `Quickstart <quickstart>`_ page, perform the basic database sync there to start to write these queries.

Block with first transaction
----------------------------

.. code :: sql

  ether_sql=# SELECT min(block_number) from blocks where transaction_count>0;
    min
    -------
    46147
    (1 row)

Total transactions in 100k blocks
---------------------------------


.. code :: sql

  ether_sql=# SELECT sum(transaction_count) from blocks where block_number < 100001;
    sum
    ---------
    26970
    (1 row)


Maximum transfer of value
-------------------------


.. code :: sql

  ether_sql=# SELECT max(value) from transactions where block_number <100001;
    max
    ----------------------------
    11901464239480000000000000
    (1 row)

.. note ::

  Someone transferred 11.9 million ether!


Transaction hash of maximum value transfer
------------------------------------------


.. code :: sql

  ether_sql=# SELECT transaction_hash from transactions where value = 11901464239480000000000000;
    transaction_hash
    --------------------------------------------------------------------
    0x9c81f44c29ff0226f835cd0a8a2f2a7eca6db52a711f8211b566fd15d3e0e8d4
    (1 row)


Total smart contracts in 100k blocks
------------------------------------

.. code :: sql

  ether_sql=# SELECT count(1) from traces where contract_address is not null and block_number < 100001;
    count
    -------
    49393
    (1 row)


Top miners in first 100k blocks
-------------------------------


.. code :: sql


  ether_sql=# SELECT miner, count(*) AS num, count(1)/100000.0 AS PERCENT
  ether_sql-# FROM blocks
  ether_sql-# WHERE block_number<=100000
  ether_sql-# GROUP BY miner
  ether_sql-# ORDER BY num DESC
  ether_sql-# LIMIT 15;
                       miner                    | num  |        percent
    --------------------------------------------+------+------------------------
    0xe6a7a1d47ff21b6321162aea7c6cb457d5476bca | 9735 | 0.09735000000000000000
    0xf927a40c8b7f6e07c5af7fa2155b4864a4112b13 | 8951 | 0.08951000000000000000
    0xbb7b8287f3f0a933474a79eae42cbca977791171 | 8712 | 0.08712000000000000000
    0x88d74a59454f6cf3b51ef6b9136afb6b9d405a88 | 4234 | 0.04234000000000000000
    0x9746c7e1ef2bd21ff3997fa467593a89cb852bd0 | 3475 | 0.03475000000000000000
    0xf8e0ca3ed80bd541b94bedcf259e8cf2141a9523 | 2409 | 0.02409000000000000000
    0xa50ec0d39fa913e62f1bae7074e6f36caa71855b | 1627 | 0.01627000000000000000
    0xbcb2e3693d246e1fc00348754334badeb88b2a11 | 1537 | 0.01537000000000000000
    0xeb1325c8d9d3ea8d74ac11f4b00f1b2367686319 | 1390 | 0.01390000000000000000
    0x1b7047b4338acf65be94c1a3e8c5c9338ad7d67c | 1335 | 0.01335000000000000000
    0xf2d2aff1320476cb8c6b607199d23175cc595693 | 1141 | 0.01141000000000000000
    0x47ff6576639c2e94762ea5443978d7681c0e78dc | 1131 | 0.01131000000000000000
    0xbb12b5a9b85d4ab8cde6056e9c1b2a4a337d2261 | 1102 | 0.01102000000000000000
    0x0037ce3d4b7f8729c8607d8d0248252be68202c0 |  917 | 0.00917000000000000000
    0x580992b51e3925e23280efb93d3047c82f17e038 |  874 | 0.00874000000000000000
    (15 rows)
