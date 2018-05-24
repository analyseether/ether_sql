from click.testing import CliRunner
from ether_sql.cli import cli


class TestEmptyDB():
    def test_create_db(self, infura_settings):
        runner = CliRunner()
        result = runner.invoke(cli, ['--settings', infura_settings,
                               'sql', 'create_tables'])
        assert result.exit_code == 0

    def test_remove_db(self, infura_settings):
        runner = CliRunner()
        result = runner.invoke(cli, ['--settings', infura_settings,
                               'sql', 'drop_tables'])
        assert result.exit_code == 0

    def test_block_number(self, infura_settings):
        runner = CliRunner()
        result = runner.invoke(cli, ['--settings', infura_settings,
                               'sql', 'blocknumber'])
        assert result.exit_code == 0
        assert result.output == 'None\n'
