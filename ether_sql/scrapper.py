from ethereum import utils
from datetime import datetime
import logging

from ether_sql import node_session, PUSH_TRACE
from ether_sql.models import Blocks, Transactions, Uncles, Receipts, Logs, Traces
from ether_sql import db_session

logger = logging.getLogger(__name__)


def add_block_number(block_number):
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
    db_session.add(block)

    transaction_list = block_data['transactions']
    uncle_list = block_data['uncles']

    for transaction_data in transaction_list:
        transaction_hash = transaction_data['hash']
        receipt_data = node_session.eth_getTransactionReceipt(transaction_hash)
        receipt = Receipts.add_receipt(receipt_data,
                                       block_number=block_number,
                                       timestamp=iso_timestamp)
        db_session.add(receipt)
        logger.debug('Reached transaction index: {}'.format(receipt.transaction_index))

        dict_logs_list = receipt_data['logs']
        for dict_log in dict_logs_list:
            log = Logs.add_log(dict_log, block_number=block_number,
                               timestamp=timestamp)
            # adding the log
            db_session.add(log)

        if PUSH_TRACE:
            dict_trace_list = node_session.trace_transaction(transaction_hash)
            if dict_trace_list is not None:
                for dict_trace in dict_trace_list:
                    trace = Traces.add_trace(dict_trace,
                                             block_number=block_number,
                                             timestamp=timestamp)
                    db_session.add(trace)

        transaction = Transactions.add_transaction(transaction_data,
                                                   block_number=block_number,
                                                   iso_timestamp=iso_timestamp)
        db_session.add(transaction)

    return db_session
