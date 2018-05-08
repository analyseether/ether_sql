from ethereum import utils
from ether_sql import node_session, PUSH_TRACE
from ether_sql.models import Blocks, Transactions, Uncles, Receipts, Logs, Traces


def add_block_number(block_number):
    """
    Adds the block, transactions, uncles, logs and traces of a given block
    number into the db_session

    :param int block_number: The block number to add to the database
    """

    # getting the block_data from the node
    block_data = node_session.eth_getBlockByNumber(block_number)
    transaction_list = block_data['transactions']
    uncle_list = block_data['uncles']
    block_data.pop('transactions', None)
    block_data.pop('uncles', None)
    timestamp = utils.parse_int_or_hex(block_data['timestamp'])

    for transaction_data in transaction_list:
        transaction_hash = transaction_data['hash']
        receipt_data = node_session.eth_getTransactionReceipt(transaction_hash)
        receipt = Receipts.add_receipt(receipt_data,
                                       block_number=block_number,
                                       timestamp=timestamp)

        dict_logs_list = receipt_data['logs']
        log_list = []
        for dict_log in dict_logs_list:
            log = Logs.add_log(dict_log, block_number=block_number,
                               timestamp=timestamp)
            log_list.append(log)

        if PUSH_TRACE:
            trace_list = []
            dict_trace_list = node_session.trace_transaction(transaction_hash)
            if dict_trace_list is not None:
                for dict_trace in dict_trace_list:
                    trace = Traces.add_trace(dict_trace,
                                             block_number=block_number,
                                             timestamp=timestamp)
                    trace_list.append(trace)
    
