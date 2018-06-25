import os
import logging
from celery import Celery
import celery.bin.base
import celery.bin.celery
import celery.platforms
from celery.signals import (
    worker_process_init,
    worker_process_shutdown,
)
import socket
import redis
from urllib.parse import urlparse
from ether_sql import settings
from ether_sql.globals import get_current_session, push_session


logger = logging.getLogger(__name__)

app = Celery('ether_sql',
             broker=settings.CELERY_BROKER,
             include='ether_sql.tasks')

app.conf.update(CELERY_RESULT_BACKEND=settings.CELERY_BACKEND,
                CELERY_TIMEZONE='UTC',
                CELERYD_LOG_FORMAT=settings.CELERYD_LOG_FORMAT,
                CELERYD_TASK_LOG_FORMAT=settings.CELERYD_TASK_LOG_FORMAT)


def celery_is_running():
    status = celery.bin.celery.CeleryCommand.commands['status']()
    status.app = status.get_app()
    try:
        status.run()
        return True
    except celery.bin.base.Error as e:
        if e.status == celery.platforms.EX_UNAVAILABLE:
            return False
        raise e


def redis_is_running():
    r = redis.from_url(settings.REDIS_URL)
    try:
        r.get(None)
        return True
    except socket.gaierror:
        logger.info('Redis is not running, using single thread')
        return False


@worker_process_init.connect
# Create a seperate session for each worker
# so that no resource is shared between them
def init_celery_session(**kwargs):
    logger.info('Initializing session for PID {}.'.format(os.getpid()))
    session = get_current_session()
    logger.info("PID {} connected to {}".format(os.getpid(), session.url))
    push_session(session)


@worker_process_shutdown.connect
def close_celery_session(**kwargs):
    current_session = get_current_session()
    try:
        current_session.db_session.close
    except AttributeError:
        logger.debug('db_session attribute does not exist')
    finally:
        pass
