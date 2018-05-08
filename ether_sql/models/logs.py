from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy import LargeBinary
import logging
from ethereum import utils
from ether_sql.models import base

logger = logging.getLogger(__name__)


class Logs(base):
    """
    Class defining a transaction in the ethereum blockchain, its properties are more
    accurately defined in the ethereum yellow paper https://github.com/ethereum/yellowpaper.


    """
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash'),
                              index=True)
    address = Column(String(42))
    data = Column(LargeBinary)
    block_number = Column(Integer, ForeignKey('blocks.block_number'))
    timestamp = Column(TIMESTAMP)
    transaction_index = Column(Integer, nullable=False)
    log_index = Column(Integer, nullable=False)
    topics_count = Column(Integer, nullable=False)
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
    def add_log(cls, log_data, block_number, timestamp):
        topics_list = log_data['topics']
        topics_count = len(topics_list)

        log = cls(transaction_hash=log_data['transactionHash'],
                  transaction_index=utils.parse_int_or_hex(log_data['transactionIndex']),
                  topics_count=topics_count,
                  address=log_data['address'],
                  log_index=utils.parse_int_or_hex(log_data['logIndex']),
                  data=log_data['data'],
                  block_number=block_number,
                  timestamp=timestamp,
                  topic_1='',
                  topic_2='',
                  topic_3='',
                  topic_4='')

        if topics_count == 1:
            log.topic_1 = topics_list[0]
        elif topics_count == 2:
            log.topic_1 = topics_list[0]
            log.topic_2 = topics_list[1]
        elif topics_count == 3:
            logger.debug(log.block_number)
            log.topic_1 = topics_list[0]
            log.topic_2 = topics_list[1]
            log.topic_3 = topics_list[2]
        elif topics_count == 4:
            log.topic_1 = topics_list[0]
            log.topic_2 = topics_list[1]
            log.topic_3 = topics_list[2]
            log.topic_4 = topics_list[3]
        elif topics_count == 0:
            logger.debug('No topics found')
        else:
            logger.error('More than 4 topics are not possible')

        return log
