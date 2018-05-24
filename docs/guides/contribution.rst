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


Updating the docs
-----------------

We suggest to create different virtual enviornment for updating the docs.

.. code :: shell

  $ virtualenv venvdocs
  $ source venvdocs/bin/activate
  $ pip install -r requirements-docs.txt
  $ pip install -e . requirements.txt

We use `Sphinx <http://www.sphinx-doc.org/en/master/>`_ to automate the documentation of python modules and `sphinx-click <https://sphinx-click.readthedocs.io/en/latest/>`_ to automate building docs of click commands.


Pull Requests
-------------

Once all the tests are passing generate a pull request and we will merge the contribution after a discussion.
