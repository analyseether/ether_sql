import os
from subprocess import call
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.globals import get_current_session
from ether_sql.models import (
    base,
)


def export_to_csv_single_thread():
    session = get_current_session()
    directory = 'test_export'
    call(["rm", "-rf", directory])
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings',
                                 session.setting_name,
                                 'sql', 'export_to_csv',
                                 '--directory', directory])
    assert result.exit_code == 0
    # match the names of exported tables
    tables_in_sql = list(base.metadata.tables)
    files_in_directory = os.listdir(directory)
    for sql_table in tables_in_sql:
        assert sql_table+'.csv' in files_in_directory
    call(["rm", "-rf", directory])


def fail_on_wrong_setting_name():
    wrong_setting_name = 'Yo'
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings',
                                 wrong_setting_name])
    print(result.output)
    assert result.exit_code is not 0
