from datetime import datetime
from celery.utils.log import get_task_logger
from celery.task import Task
from celery.signals import task_prerun
from web3.utils.encoding import to_int
from ether_sql.globals import get_current_session
from ether_sql.tasks.worker import app
from ether_sql.models import (
    Blocks,
    Transactions,
    Uncles,
    Receipts,
    Logs,
    Traces,
    MetaInfo,
    StateDiff,
    BlockTaskMeta,
)

logger = get_task_logger(__name__)


class BlockTaskTracker(Task):
    def on_success(self, retval, task_id, args, kwargs):
        current_session = get_current_session()
        with current_session.db_session_scope():
            block_task_meta = BlockTaskMeta.get_block_task_meta_from_task_id(current_session, task_id)
            for i_block_task_meta in block_task_meta:
                if i_block_task_meta.block_hash == retval or i_block_task_meta is None:
                    i_block_task_meta.state = 'SUCCESS'
                    current_session.db_session.add(i_block_task_meta)
                else:
                    i_block_task_meta.state = 'FORKED'
                    current_session.db_session.add(i_block_task_meta)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        current_session = get_current_session()
        with current_session.db_session_scope():
            block_task_meta = BlockTaskMeta.get_block_task_meta_from_task_id(current_session, task_id)
            block_task_meta.state = 'FAILURE'
            current_session.db_session.add(block_task_meta)


def scrape_blocks(list_block_numbers, mode):
    """
    Function which starts scrapping data from the node and pushes it into
    the sql database

    :param list list_block_numbers: List of block numbers to push in the database
    :param str mode: Mode to be used weather parallel or single
    """
    task_list = []
    current_session = get_current_session()
    for block_number in list_block_numbers:
        logger.debug('Adding block: {}'.format(block_number))
        if mode == 'parallel':
            r = add_block_number.delay(block_number)
            task_list.append(r)
            block_task_meta = BlockTaskMeta(task_id=r.id,
                                            task_name='add_block_number',
                                            state='PENDING',
                                            block_number=block_number)
            with current_session.db_session_scope():
                current_session.db_session.add(block_task_meta)
        elif mode == 'single':
            add_block_number(block_number)
        else:
            raise ValueError('Mode {} is unavailable'.format(mode))
    return task_list


@app.task(base=BlockTaskTracker, max_retries=5)
def add_block_number(block_number):
    """
    Adds the block, transactions, uncles, logs and traces of a given block
    number into the db_session

    :param int block_number: The block number to add to the database
    """
    current_session = get_current_session()
    with current_session.db_session_scope():
        block_task_meta = BlockTaskMeta.update_block_task_meta_from_block_number(
            current_session=current_session,
            block_number=block_number,
            state='STARTED')

    # getting the block_data from the node
    block_data = current_session.w3.eth.getBlock(
                            block_identifier=block_number,
                            full_transactions=True)
    timestamp = to_int(block_data['timestamp'])
    iso_timestamp = datetime.utcfromtimestamp(timestamp).isoformat()
    block = Blocks.add_block(block_data=block_data,
                             iso_timestamp=iso_timestamp)
    block_hash = block.block_hash

    if current_session.settings.PARSE_TRACE and \
       current_session.settings.PARSE_STATE_DIFF and \
       block_number != 0:
        block_trace_list = current_session.w3.parity.\
            traceReplayBlockTransactions(block_number,
                                         mode=['trace', 'stateDiff'])
    elif block_number != 0:
        if current_session.settings.PARSE_TRACE:
            block_trace_list = current_session.w3.parity.\
                traceReplayBlockTransactions(block_number,
                                             mode=['trace'])

        if current_session.settings.PARSE_STATE_DIFF:
            block_trace_list = current_session.w3.parity.\
                traceReplayBlockTransactions(block_number,
                                             mode=['stateDiff'])

    # added the block data in the db session
    with current_session.db_session_scope():
        current_session.db_session.add(block)

        uncle_hashes = block_data['uncles']
        uncle_list = []
        for i in range(0, len(uncle_hashes)):
            # Unfortunately there is no command eth_getUncleByHash
            uncle_data = current_session.w3.eth.getUncleByBlock(
                                block_number, i)
            uncle = Uncles.add_uncle(uncle_data=uncle_data,
                                     block_number=block_number,
                                     iso_timestamp=iso_timestamp)
            current_session.db_session.add(uncle)
            uncle_list.append(uncle)

        transaction_list = block_data['transactions']
        # loop to get the transaction, receipts, logs and traces of the block
        for index, transaction_data in enumerate(transaction_list):
            transaction = Transactions.add_transaction(transaction_data,
                                                       block_number=block_number,
                                                       iso_timestamp=iso_timestamp)
            # added the transaction in the db session
            current_session.db_session.add(transaction)

            receipt_data = current_session.w3.eth.getTransactionReceipt(
                                    transaction_data['hash'])
            receipt = Receipts.add_receipt(receipt_data,
                                           block_number=block_number,
                                           timestamp=iso_timestamp)
            current_session.db_session.add(receipt)
            fees = int(transaction.gas_price)*int(receipt.gas_used)

            log_list = receipt_data['logs']
            Logs.add_log_list(current_session=current_session,
                              log_list=log_list,
                              block_number=block_number,
                              timestamp=transaction.timestamp)

            if current_session.settings.PARSE_TRACE:
                trace_list = block_trace_list[index]['trace']
                Traces.add_trace_list(
                        current_session=current_session,
                        trace_list=trace_list,
                        transaction_hash=transaction.transaction_hash,
                        transaction_index=transaction.transaction_index,
                        block_number=transaction.block_number,
                        timestamp=transaction.timestamp)

            if current_session.settings.PARSE_STATE_DIFF:
                state_diff_dict = block_trace_list[index]['stateDiff']
                if state_diff_dict is not None:
                    StateDiff.add_state_diff_dict(
                        current_session=current_session,
                        state_diff_dict=state_diff_dict,
                        transaction_hash=transaction.transaction_hash,
                        transaction_index=transaction.transaction_index,
                        block_number=transaction.block_number,
                        timestamp=transaction.timestamp,
                        miner=block.miner,
                        fees=fees)
        if block_number == 0:
            StateDiff.parse_genesis_rewards(current_session=current_session,
                                            block=block)
        else:
            StateDiff.add_mining_rewards(current_session=current_session,
                                         block=block,
                                         uncle_list=uncle_list)
        # updating the meta info table
        MetaInfo.set_last_pushed_block(current_session, block_number)
    logger.info("Commiting block: {} to sql".format(block_number))
    return block_hash


@app.task()
def remove_block_number(block_number):
    """
    Removes the block, transactions, uncles, logs and traces of a given block
    number into the database to perform chain reorgs.

    :param int block_number: The block number to add to the database
    """
    current_session = get_current_session()
    with current_session.db_session_scope():
        current_session.db_session.query(Blocks).\
            filter_by(block_number=block_number).delete()
        logger.info("Removed block {}".format(block_number))
