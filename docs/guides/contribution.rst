Contributing
============
Thank you for your interest in contributing! Please read along to learn how to get started.


Running the tests
-----------------

We create a seperate database to run our tests, so it does not interfere with the current synced database.

Use the following command to create a new database:

.. code :: shell

  $ createdb ether_sql_tests


All our tests can be run using the following command:


.. code :: shell

  $ python -m pytest ether_sql/tests/


Pull Requests
-------------

Once all the tests are passing generate a pull request and we will merge the contribution after a discussion.
