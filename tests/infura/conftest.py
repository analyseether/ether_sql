import pytest
from ether_sql.setup import Session
from ether_sql.models import base

pytest_plugins = [
   "tests.fixtures.expected_data",
]


@pytest.fixture(scope='function')
def infura_settings():
    infura_settings = 'TestSettings'
    return infura_settings


@pytest.fixture(scope='function')
def empty_db_infura_session(infura_settings):
    """
    Infura Fixture containing exmpty database
    """
    empty_db_infura_session = Session(override_settings=infura_settings)
    return empty_db_infura_session


@pytest.fixture(scope='function')
def empty_table_infura_session(empty_db_infura_session):
    """
    Infura Fixture with created but empty tables
    """
    empty_table_infura_session = empty_db_infura_session
    base.metadata.create_all(empty_table_infura_session.db_engine)
    return empty_table_infura_session
