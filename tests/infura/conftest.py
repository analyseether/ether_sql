import pytest
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session

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


@pytest.fixture(scope='function')
def infura_session_block_56160(infura_settings):
    """
    Infura session with block 56160 in psql
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', infura_settings,
                        'scrape_block', '--block_number', 56160])
    return infura_session_block_56160
