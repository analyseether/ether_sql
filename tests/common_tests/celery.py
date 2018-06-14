import os
from subprocess import call
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.tasks.worker import celery_is_running
from ether_sql.models import base


def export_to_csv_multiple_threads(node_session_block_56160):
    # assert celery_is_running()
    # assert redis_is_running()
    directory = 'test_export'
    call(["rm", "-rf", directory])
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings',
                                 node_session_block_56160.setting_name,
                                 'sql', 'export_to_csv',
                                 '--directory', directory])
    assert result.exit_code == 0
    # match the names of exported tables
    tables_in_sql = list(base.metadata.tables)
    files_in_directory = os.listdir(directory)
    for sql_table in tables_in_sql:
        assert sql_table+'.csv' in files_in_directory
    call(["rm", "-rf", directory])


def push_block_range_multiple_threads(settings_name):
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings', settings_name,
                                 'scrape_block_range',
                                 '--start_block_number', 0,
                                 '--end_block_number', 10])
    assert result.exit_code == 0
    assert celery_is_running()
