from click.testing import CliRunner
from ether_sql.cli import cli


class TestEtherCli():

    def test_listening_to_infura_node(self, parity_session):
        listening = parity_session.w3.isConnected()
        assert listening is True

    def test_ether_block_number(self,
                                parity_settings,
                                parity_session):
        runner = CliRunner()
        result = runner.invoke(cli, ['--settings', parity_settings,
                               'ether', 'blocknumber'])
        assert result.exit_code == 0
