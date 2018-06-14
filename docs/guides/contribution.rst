Contributing
============
Thank you for your interest in contributing! Please read along to learn how to get started.


Running the tests
-----------------

We create a seperate database to run our tests, so it does not interfere with the current synced database.

Use the following command to create a new database:

.. code :: shell

  $ createdb ether_sql_tests

If you are testing using Infura node use the command:

.. code :: shell

  $ python -m pytest tests/infura

If you are using a local parity node use the command:

.. code :: shell

  $ python -m pytest tests/parity


Updating the database tables
----------------------------

We use `Alembic <http://alembic.zzzcomputing.com/en/latest/tutorial.html>`_ to
handle database migrations.

You can create new tables by adding a new class in the :code:`ether_sql/models` module. More details on available columns are available at `SQLAlchemy guides <http://docs.sqlalchemy.org/en/latest/orm/tutorial.html>`_

To create SQL commands that can reflect the changes in the database, run the following command.


.. code :: shell

  $ ether_sql sql migrate -m "message for changes"

Next upgrade the database using the following command:

.. code :: shell

  $ ether_sql sql upgrade

Updating the docs
-----------------

We suggest to create different virtual enviornment for updating the docs.

.. code :: shell

  $ virtualenv venvdocs
  $ source venvdocs/bin/activate
  $ pip install -e . requirements.txt

We use `Sphinx <http://www.sphinx-doc.org/en/master/>`_ to automate the documentation of python modules and `sphinx-click <https://sphinx-click.readthedocs.io/en/latest/>`_ to automate building docs of click commands.


Pull Requests
-------------

Once all the tests are passing generate a pull request and we will merge the contribution after a discussion.
