import logging
import time
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session
from ether_sql.tasks.worker import app
from .celery_worker_thread import CeleryWorkerThread


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


def celery_worker_thread(settings_name):
    """
    Common fixture which starts celery workers in seperate threads
    """
    celery_worker_thread = CeleryWorkerThread(app, settings=settings_name)
    celery_worker_thread.setDaemon(True)
    celery_worker_thread.start()
    celery_worker_thread.ready.wait()
    time.sleep(1)
    return celery_worker_thread
