import time
import subprocess
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.tasks.worker import app

def celery_worker(settings_name):
    """py.test fixture to shoot up Celery worker process to process test tasks."""
    app.control.purge()

    cmdline = "ether_sql --settings={} celery start -c1 -n worker1@".format(settings_name)

    # logger.info("Running celery worker: %s", cmdline)

    worker = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(4.0)
    worker.poll()

    return worker

def celery_filter_worker(settings_name):
    """py.test fixture to shoot up Celery worker process to process test tasks."""
    app.control.purge()

    cmdline = "ether_sql --settings={} celery start -c1 -B -Q celery_filters".format(settings_name)

    # logger.info("Running celery worker: %s", cmdline)

    worker = subprocess.Popen(cmdline, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True,
                              encoding='utf8')
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
