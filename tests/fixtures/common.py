import logging
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session
from ether_sql.tasks.worker import app, celery_is_running
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


def session_block_56160(settings_name):
    """
    Common fixture with the data of block 56160
    """
    runner = CliRunner()
    runner.invoke(cli, ['--settings', settings_name,
                        'scrape_block', '--block_number', 56160])
    session_block_56160 = Session(settings_name)
    return session_block_56160


def celery_worker_thread(settings_name):
    """
    Common fixture which starts celery workers in seperate threads
    """
    celery_worker_thread = CeleryWorkerThread(app, settings=settings_name)
    celery_worker_thread.daemon = True
    celery_worker_thread.start()
    return celery_worker_thread
