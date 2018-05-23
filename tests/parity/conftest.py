import pytest

from ether_sql.session import Session
from ether_sql.models import base

pytest_plugins = [
   "tests.fixtures.expected_data",
]


@pytest.fixture(scope='function')
def parity_settings():
    infura_settings = 'ParityTestSettings'
    return infura_settings


@pytest.fixture(scope='function')
def empty_db_parity_session(parity_settings):
    """
    Parity Fixture containing exmpty database
    """
    empty_db_parity_session = Session(settings=parity_settings)
    return empty_db_parity_session


@pytest.fixture(scope='function')
def empty_table_parity_session(empty_db_parity_session):
    """
    Parity Fixture with created but empty tables
    """
    empty_table_parity_session = empty_db_parity_session
    base.metadata.create_all(empty_table_parity_session.db_engine)
    return empty_table_parity_session
