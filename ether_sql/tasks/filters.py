import logging
from celery.utils.log import get_task_logger
from ether_sql.globals import get_current_session
from ether_sql.tasks.worker import app
from ether_sql.models import BlockTaskMeta
from web3.utils.encoding import to_int, to_hex
from ether_sql.tasks.scrapper import add_block_number


logger = get_task_logger(__name__)



@app.task()
def new_blocks():
    """
    Celery beat task which runs every second to get new blocks.
    :param block_filter: block filter as described in session.py
    """
    current_session = get_current_session()
    logger.debug("Reached at new blocks to get block hashes")
    block_hashes = current_session.block_filter.get_new_entries()
    for block_hash in block_hashes:
        block_data = current_session.w3.eth.getBlock(block_hash)
        block_number = to_int(block_data['number'])
        BlockTaskMeta.add_block_task_meta(task_name='new_blocks',
                              state='WAITING',
                              block_number=block_number,
                              block_hash=to_hex(block_hash))
    logger.info(block_hashes)

@app.task()
def push_blocks_in_queue():
    """
    Celery beat task which runs every 30 second to check for blocks which are
    settings.BLOCK_LAG number of blocks behind the current ethereum client and
    pushes the blocks in waiting to the queue.
    """
    current_session = get_current_session()
    with current_session.db_session_scope():
        blocks_in_waiting = BlockTaskMeta.get_blocks_to_be_pushed_in_queue(
                                current_session)
        for blocks in blocks_in_waiting:
            block_number = int(blocks.block_number)
            add_block_task = add_block_number.delay(block_number)
            BlockTaskMeta.update_block_task_meta_from_block_number(
                current_session=current_session,
                block_number=block_number,
                task_id=add_block_task.id,
                state='PENDING',
                task_name='add_block_number')
