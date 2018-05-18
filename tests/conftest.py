from ether_sql import setup_db_engine
from ether_sql import base
from ether_sql import settings
import pytest

# SQLALCHEMY settings
TEST_SQLALCHEMY_DB = 'ether_sql_tests'


@pytest.fixture()
def empty_sql_engine():
    """
    Fixture containing exmpty database
    """
    empty_sql_engine = setup_db_engine(user=settings.SQLALCHEMY_USER,
                                       password=settings.SQLALCHEMY_PASSWORD,
                                       db=TEST_SQLALCHEMY_DB)
    return empty_sql_engine


@pytest.fixture()
def empty_table_engine():
    """
    Fixture with created but empty tables
    """
    empty_table_engine = setup_db_engine(user=settings.SQLALCHEMY_USER,
                                         password=settings.SQLALCHEMY_PASSWORD,
                                         db=TEST_SQLALCHEMY_DB)

    base.metadata.create_all(empty_table_engine)

    return empty_table_engine
