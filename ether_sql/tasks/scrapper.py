from datetime import datetime
from celery.utils.log import get_task_logger
from web3.utils.encoding import to_int, to_hex
from ether_sql.globals import get_current_session
from ether_sql.tasks.worker import celery
from ether_sql.models import (
    Blocks,
    Transactions,
    Uncles,
    Receipts,
    Logs,
    Traces,
    MetaInfo,
)

logger = get_task_logger(__name__)


def scrape_blocks(start_block_number, end_block_number, mode):
    """
    Main function which starts scrapping data from the node and pushes it into
    the sql database

    :param int start_block_number: starting block number of scraping
    :param int end_block_number: end block number of scraping
    """

    logger.debug("Start block: {}".format(start_block_number))
    logger.debug('End block: {}'.format(end_block_number))

    r = None
    for block_number in range(start_block_number, end_block_number+1):
        logger.debug('Adding block: {}'.format(block_number))
        if mode == 'parallel':
            r = add_block_number.delay(block_number)
        elif mode == 'single':
            add_block_number(block_number)
        else:
            raise ValueError('Mode {} is unavailable'.format(mode))
    return r


@celery.task()
def add_block_number(block_number):
    """
    Adds the block, transactions, uncles, logs and traces of a given block
    number into the db_session

    :param int block_number: The block number to add to the database
    """
    current_session = get_current_session()
    current_session.setup_db_session()

    # getting the block_data from the node
    block_data = current_session.w3.eth.getBlock(
                            block_identifier=block_number,
                            full_transactions=True)
    timestamp = to_int(block_data['timestamp'])
    iso_timestamp = datetime.utcfromtimestamp(timestamp).isoformat()
    block = Blocks.add_block(block_data=block_data,
                             iso_timestamp=iso_timestamp)
    current_session.db_session.add(block)  # added the block data in the db session

    logger.debug('Reached this spot')
    transaction_list = block_data['transactions']
    # loop to get the transaction, receipts, logs and traces of the block
    for transaction_data in transaction_list:
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

        current_session.db_session.add(receipt)  # added the receipt in the database

        logs_list = receipt_data['logs']
        for dict_log in logs_list:
            log = Logs.add_log(dict_log, block_number=block_number,
                               iso_timestamp=iso_timestamp)
            current_session.db_session.add(log)  # adding the log in db session

        if current_session.settings.PARSE_TRACE:
            dict_trace_list = current_session.w3.parity.traceTransaction(
                                           to_hex(transaction_data['hash']))
            if dict_trace_list is not None:
                for dict_trace in dict_trace_list:
                    trace = Traces.add_trace(dict_trace,
                                             block_number=block_number,
                                             timestamp=iso_timestamp)
                    current_session.db_session.add(trace)  # added the trace in the db session

    uncle_list = block_data['uncles']
    for i in range(0, len(uncle_list)):
        # Unfortunately there is no command eth_getUncleByHash
        uncle_data = current_session.w3.eth.getUncleByBlock(
                                  block_number, i)
        uncle = Uncles.add_uncle(uncle_data=uncle_data,
                                 block_number=block_number,
                                 iso_timestamp=iso_timestamp)
        current_session.db_session.add(uncle)

    meta_info = current_session.db_session.query(MetaInfo).first()
    if meta_info is None:
        # No rows have been inserted yet
        meta_info = MetaInfo(last_pushed_block=block_number)
    else:
        meta_info.last_pushed_block = block_number
    current_session.db_session.add(meta_info)
    logger.debug('{}'.format(meta_info.to_dict()))

    logger.info("Commiting block: {} to sql".format(block_number))
    current_session.db_session_safe_commit()
