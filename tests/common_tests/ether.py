from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session


def listening_to_node(settings_name):
    session = Session(settings_name)
    listening = session.w3.isConnected()
    assert listening is True


def ether_block_number(settings_name):
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings', settings_name,
                           'ether', 'blocknumber'])
    assert result.exit_code == 0
