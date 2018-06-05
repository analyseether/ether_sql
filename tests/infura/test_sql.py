import os
from click.testing import CliRunner
from ether_sql.cli import cli
from subprocess import call
from sqlalchemy import MetaData
from ether_sql.models import base


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


class TestOneBlockDb():

    def test_export_to_csv(self,
                           infura_settings):
        directory = 'test_export'
        call(["rm", "-rf", directory])
        runner = CliRunner()
        runner.invoke(cli, ['--settings', infura_settings,
                            'scrape_block', '--block_number', 56160])
        result = runner.invoke(cli, ['--settings', infura_settings,
                                     'sql', 'export_to_csv',
                                     '--directory', directory])
        assert result.exit_code == 0
        # match the names of exported tables
        tables_in_sql = list(base.metadata.tables)
        files_in_directory = os.listdir(directory)
        for sql_table in tables_in_sql:
            assert sql_table+'.csv' in files_in_directory
        call(["rm", "-rf", directory])
