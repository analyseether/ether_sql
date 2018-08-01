import logging
from celery.utils.log import get_task_logger
from ether_sql.globals import get_current_session
from ether_sql.tasks.worker import app


logger = get_task_logger(__name__)


@app.task()
def new_blocks():
    """
    Celery beat task which runs every second to get new blocks.

    :param block_filter: block filter as described in worker.py
    """
    current_session = get_current_session()
    block = current_session.block_filter.get_new_entries()
    logger.info(block)
