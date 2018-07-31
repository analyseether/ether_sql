import os
import logging
import time
from subprocess import call
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.models import base
from ether_sql.globals import get_current_session
from ether_sql.tasks.scrapper import scrape_blocks
from tests.common_tests.blocks import verify_block_range_56160_56170


logger = logging.getLogger(__name__)


def push_block_range_multiple_thread():
    list_block_numbers = list(range(56160, 56171))
    task_list = scrape_blocks(list_block_numbers=list_block_numbers,
                              mode='parallel')
    for task in task_list:
        task.wait()
    verify_block_range_56160_56170()


def export_to_csv_multiple_threads(settings_name):
    # assert celery_is_running()
    # assert redis_is_running()
    directory = 'test_export'
    call(["rm", "-rf", directory])
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings',
                                 settings_name,
                                 'sql', 'export_to_csv',
                                 '--directory', directory,
                                 '--mode', 'parallel'])
    assert result.exit_code == 0
    time.sleep(4)
    # match the names of exported tables
    tables_in_sql = list(base.metadata.tables)
    files_in_directory = os.listdir(directory)
    for sql_table in tables_in_sql:
        assert sql_table+'.csv' in files_in_directory
    call(["rm", "-rf", directory])
