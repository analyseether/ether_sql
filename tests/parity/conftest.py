import pytest
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session


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
    infura_session = Session(parity_settings)
    return infura_session


@pytest.fixture(scope='function')
def parity_session_block_56160(parity_settings):
    """
    Parity session with block 56160 in psql
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', parity_settings,
                        'scrape_block', '--block_number', 56160])
    return parity_session_block_56160
