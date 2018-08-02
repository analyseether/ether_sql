from sqlalchemy import Column, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy import Text, Integer
import logging
from eth_utils import to_checksum_address
from web3.utils.encoding import to_int, to_hex
from ether_sql.models import base

logger = logging.getLogger(__name__)


class Logs(base):
    """
    Class mapping a log table in the psql database to a log in ethereum node.

    :param str transaction_hash: Hash of the transaction which created this log
    :param str address: Address from which this log originated
    :param str data: Contains one or more 32 Bytes non-indexed arguelents of the log
    :param int block_number: The block number where this transaction was included
    :param datetime timestamp: Timestamp when the block was mined
    :param int transaction_index: Position of the transaction in the block
    :param int log_index: Position of the log in the block
    :param int topics_count: Total number of topics in this log
    :param str topic_1: First topic in the log
    :param str topic_2: Second topic in the log
    :param str topic_3: Third topic in the log
    :param str topic_4: Fourth topic in the log

    """
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash', ondelete='CASCADE'),
                              index=True)
    address = Column(String(42), nullable=False)
    data = Column(Text)
    block_number = Column(Numeric, ForeignKey('blocks.block_number', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP)
    transaction_index = Column(Numeric, nullable=False)
    log_index = Column(Numeric, nullable=False)
    topics_count = Column(Numeric, nullable=False)
    topic_1 = Column(String(66), nullable=True)
    topic_2 = Column(String(66), nullable=True)
    topic_3 = Column(String(66), nullable=True)
    topic_4 = Column(String(66), nullable=True)

    def to_dict(self):
        return {
                'transaction_hash': self.transaction_hash,
                'address': self.address,
                'data': self.data,
                'block_number': self.block_number,
                'timestamp': self.timestamp,
                'transaction_index': self.transaction_index,
                'log_index': self.log_index,
                'topics_count': self.topics_count,
                'topic_1': self.topic_1,
                'topic_2': self.topic_2,
                'topic_3': self.topic_3,
                'topic_4': self.topic_4
        }

    @classmethod
    def add_log(cls, log_data, block_number, iso_timestamp):
        """
        Creates a new log object from data received from JSON-RPC call
        eth_getTransactionReceipt.

        :param dict log_data: data received from receipt JSON RPC call
        :param int block_number: block number of the block containing the log
        :param datetime iso_timestamp: timestamp when the block containing the transaction was mined

        """
        topics_count = len(log_data['topics'])

        log = cls(transaction_hash=to_hex(log_data['transactionHash']),
                  transaction_index=to_int(log_data['transactionIndex']),
                  topics_count=topics_count,
                  address=to_checksum_address(log_data['address']),
                  log_index=to_int(log_data['logIndex']),
                  data=log_data['data'],
                  block_number=block_number,
                  timestamp=iso_timestamp,
                  topic_1='',
                  topic_2='',
                  topic_3='',
                  topic_4='')

        if topics_count == 0:
            logger.warn('No topics present')
        elif topics_count == 1:
            log.topic_1 = to_hex(log_data['topics'][0])
        elif topics_count == 2:
            log.topic_1 = to_hex(log_data['topics'][0])
            log.topic_2 = to_hex(log_data['topics'][1])
        elif topics_count == 3:
            log.topic_1 = to_hex(log_data['topics'][0])
            log.topic_2 = to_hex(log_data['topics'][1])
            log.topic_3 = to_hex(log_data['topics'][2])
        elif topics_count == 4:
            log.topic_1 = to_hex(log_data['topics'][0])
            log.topic_2 = to_hex(log_data['topics'][1])
            log.topic_3 = to_hex(log_data['topics'][2])
            log.topic_4 = to_hex(log_data['topics'][3])
        else:
            logger.error('More than 4 topics are not possible')

        logger.debug("tx_hash: {}, log_index: {}".format(log.transaction_hash, log.log_index))

        return log

    @classmethod
    def add_log_list(cls, current_session, log_list, block_number, timestamp):
        """
        Adds a list of logs in the session
        """
        for log_data in log_list:
            log = cls.add_log(log_data=log_data,
                              block_number=block_number,
                              iso_timestamp=timestamp)
            # adding the log in db session
            current_session.db_session.add(log)
