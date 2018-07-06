import logging
import time
import subprocess
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session


logger = logging.getLogger(__name__)


def session_settings(settings_name):
    """
    Settings with empty tables
    """
    session_settings = settings_name
    runner = CliRunner()
    runner.invoke(cli, ['--settings', session_settings,
                        'sql', 'upgrade_tables'])
    return session_settings


def drop_session_tables(settings_name):
    """
    Droping all tables
    """
    session_settings = settings_name
    runner = CliRunner()
    runner.invoke(cli, ['--settings', session_settings,
                        'sql', 'drop_tables'])


def session_block_56160(settings_name):
    """
    Common fixture with the data of block 56160
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', settings_name,
                        'scrape_block', '--block_number', 56160])
    session_block_56160 = Session(settings_name)
    return session_block_56160


def session_block_range_56160_56170(settings_name):
    """
    Common fixture with data between block 56160 and 56170
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', settings_name,
                        'scrape_block_range',
                        '--start_block_number', 56160,
                        '--end_block_number', 56170])
    session_block_range_56160_56170 = Session(settings_name)
    return session_block_range_56160_56170


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
