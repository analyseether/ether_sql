import pytest
import logging
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session

logger = logging.getLogger(__name__)

pytest_plugins = [
   "tests.fixtures.expected_data",
]


@pytest.fixture(scope='function')
def parity_settings():
    """
    Parity test settings with empty tables
    """
    infura_settings = 'ParityTestSettings'
    runner = CliRunner()
    logger.debug('Dropping tables')
    # Deleting and creating tables
    runner.invoke(cli, ['--settings', infura_settings,
                        'sql', 'drop_tables'])
    runner.invoke(cli, ['--settings', infura_settings,
                        'sql', 'create_tables'])
    return infura_settings


@pytest.fixture(scope='function')
def parity_session(parity_settings):
    """
    Parity test session with created but empty tables
    """
    parity_session = Session(parity_settings)
    return parity_session
