from ethereum import utils
from datetime import datetime
import logging

from ether_sql import node_session, PUSH_TRACE, db_engine
from ether_sql.models import Blocks, Transactions, Uncles, Receipts, Logs
from ether_sql.models import Traces
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def scrape_blocks(session, sql_block_number=None, node_block_number=None):
    """
    Main function which starts scrapping data from the node and pushes it into
    the sql database

    :param int sql_block_number: starting block number of scraping
    :param int node_block_number: end block number of scraping
    """

    logger.debug("Start block: {}".format(sql_block_number))
    logger.debug('End block: {}'.format(node_block_number))

    for block_number in range(sql_block_number+1, node_block_number+1):
        logger.debug('Adding block: {}'.format(block_number))

        session = add_block_number(block_number=block_number,
                                   session=session)
        logger.info("Commiting block: {} to sql".format(block_number))
        session.commit()


def add_block_number(block_number, session):
    """
    Adds the block, transactions, uncles, logs and traces of a given block
    number into the db_session

    :param int block_number: The block number to add to the database
    """

    # getting the block_data from the node
    block_data = node_session.eth_getBlockByNumber(block_number)
    timestamp = utils.parse_int_or_hex(block_data['timestamp'])
    iso_timestamp = datetime.fromtimestamp(timestamp).isoformat()
    block = Blocks.add_block(block_data=block_data, iso_timestamp=iso_timestamp)
    session.add(block)  # added the block data in the db session

    transaction_list = block_data['transactions']
    # loop to get the transaction, receipts, logs and traces of the block
    for transaction_data in transaction_list:
        transaction = Transactions.add_transaction(transaction_data,
                                                   block_number=block_number,
                                                   iso_timestamp=iso_timestamp)
        session.add(transaction)  # added the transaction in the db session

        receipt_data = node_session.eth_getTransactionReceipt(
                                    transaction_data['hash'])
        receipt = Receipts.add_receipt(receipt_data,
                                       block_number=block_number,
                                       timestamp=iso_timestamp)

        session.add(receipt)  # added the receipt in the database

        logs_list = receipt_data['logs']
        for dict_log in logs_list:
            log = Logs.add_log(dict_log, block_number=block_number,
                               iso_timestamp=iso_timestamp)
            session.add(log)  # adding the log in db session

        if PUSH_TRACE:
            dict_trace_list = node_session.trace_transaction(
                                           transaction_data['hash'])
            if dict_trace_list is not None:
                for dict_trace in dict_trace_list:
                    trace = Traces.add_trace(dict_trace,
                                             block_number=block_number,
                                             timestamp=iso_timestamp)
                    session.add(trace)  # added the trace in the db session

    uncle_list = block_data['uncles']
    for i in range(0, len(uncle_list)):
        # Unfortunately there is no command eth_getUncleByHash
        uncle_data = node_session.eth_getUncleByBlockNumberAndIndex(
                                  block_number, i)
        uncle = Uncles.add_uncle(uncle_data=uncle_data,
                                 block_number=block_number,
                                 iso_timestamp=iso_timestamp)
        session.add(uncle)

    return session
