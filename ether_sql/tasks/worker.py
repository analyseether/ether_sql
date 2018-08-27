import os
import logging
from celery import Celery
from celery.signals import (
    worker_process_init,
    worker_process_shutdown,
)
from kombu import Queue
from datetime import timedelta
from ether_sql import settings
from ether_sql.globals import get_current_session, push_session


logger = logging.getLogger(__name__)

app = Celery('ether_sql',
             broker=settings.CELERY_BROKER,
             include='ether_sql.tasks')

celery_schedule = {
    'new_blocks': {
        'task': 'ether_sql.tasks.filters.new_blocks',
        'schedule': timedelta(seconds=30),
        'options': {'queue' : 'celery_filters'}
    },
    'push_blocks_in_queue': {
        'task': 'ether_sql.tasks.filters.push_blocks_in_queue',
        'schedule': timedelta(seconds=30),
        'options': {'queue' : 'celery_filters'}
    },
}

app.conf.update(CELERY_RESULT_BACKEND=settings.CELERY_BACKEND,
                CELERY_TIMEZONE='UTC',
                CELERYD_LOG_FORMAT=settings.CELERYD_LOG_FORMAT,
                CELERYD_TASK_LOG_FORMAT=settings.CELERYD_TASK_LOG_FORMAT,
                CELERYBEAT_SCHEDULE = celery_schedule,
                CELERY_ACKS_LATE=True)


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
