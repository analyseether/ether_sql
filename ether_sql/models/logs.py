from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy import LargeBinary

from ether_sql.models import base


class Logs(base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash'),
                              index=True)
    address = Column(String(42))
    data = Column(LargeBinary)
    block_number = Column(Integer, ForeignKey('blocks.block_number'))
    timestamp = Column(TIMESTAMP, ForeignKey('blocks.timestamp'))
    transaction_index = Column(Integer, nullable=False)
    transaction_log_index = Column(Integer, nullable=False)
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
                'transaction_log_index': self.transaction_log_index,
                'log_index': self.log_index,
                'topics_count': self.topics_count,
                'topic_1': self.topic_1,
                'topic_2': self.topic_2,
                'topic_3': self.topic_3,
                'topic_4': self.topic_4
        }
