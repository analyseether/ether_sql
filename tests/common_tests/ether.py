from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session


def listening_to_node(setting_name):
    session = Session(setting_name)
    listening = session.w3.isConnected()
    assert listening is True


def ether_block_number(setting_name):
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings', setting_name,
                           'ether', 'blocknumber'])
    assert result.exit_code == 0
