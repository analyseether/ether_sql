import pytest
import logging
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session

logger = logging.getLogger(__name__)

# This will include all fixtures in fixtures directory
pytest_plugins = [
   "tests.fixtures.expected_data",
]


@pytest.fixture(scope='function')
def infura_settings():
    """
    Infura settings with empty tables
    """
    infura_settings = 'TestSettings'
    runner = CliRunner()
    logger.debug('Dropping tables')
    # Deleting and creating tables
    runner.invoke(cli, ['--settings', infura_settings,
                        'sql', 'drop_tables'])
    runner.invoke(cli, ['--settings', infura_settings,
                        'sql', 'create_tables'])
    return infura_settings


@pytest.fixture(scope='function')
def infura_session(infura_settings):
    """
    Infura session with created but empty tables
    """
    infura_session = Session(infura_settings)
    return infura_session
