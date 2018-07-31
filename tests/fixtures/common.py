import logging
import time
import subprocess
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session
from ether_sql.globals import push_session
from tests.common_tests.utils import add_block


logger = logging.getLogger(__name__)


def session_settings(setting_name):
    """
    Settings with empty tables
    """
    runner = CliRunner()
    drop_session_tables(setting_name)
    runner.invoke(cli, ['--settings', setting_name,
                        'sql', 'upgrade_tables'])
    return setting_name


def drop_session_tables(setting_name):
    """
    Droping all tables
    """
    session_settings = setting_name
    runner = CliRunner()
    runner.invoke(cli, ['--settings', session_settings,
                        'sql', 'drop_tables'])


def session_block_56160(setting_name):
    """
    Common fixture with the data of block 56160
    """
    add_block(setting_name, 56160)
    session = Session(setting_name)
    push_session(session=session)


def session_block_range_56160_56170(setting_name):
    """
    Common fixture with data between block 56160 and 56170
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', setting_name,
                        'scrape_block_range',
                        '--start_block_number', 56160,
                        '--end_block_number', 56170,
                        '--no-fill_gaps'])
    session = Session(setting_name)
    push_session(session=session)


def celery_worker(settings_name):
    """py.test fixture to shoot up Celery worker process to process test tasks."""

    cmdline = "ether_sql --settings={} celery start -c1".format(settings_name)

    # logger.info("Running celery worker: %s", cmdline)

    worker = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(4.0)
    worker.poll()

    return worker


def celery_shutdown(settings_name):
    """
    Teardown function to shutdown running celery workers
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', settings_name,
                        'celery', 'shutdown'])


def session_missing_blocks(setting_name):
    """
    Common fixture which creates missing blocks in the database
    """
    add_block(setting_name, 0)
    add_block(setting_name, 2)
    add_block(setting_name, 4)
    runner = CliRunner()
    runner.invoke(cli, ['--settings', setting_name,
                        'scrape_block_range',
                        '--end_block_number', 10,
                        '--no-fill_gaps'])
    session = Session(setting_name)
    push_session(session=session)


def session_first_10_blocks(setting_name):
    """
    Common fixture which creates missing blocks in the database
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', setting_name,
                        'scrape_block_range',
                        '--end_block_number', 10])
    session = Session(setting_name)
    push_session(session=session)
