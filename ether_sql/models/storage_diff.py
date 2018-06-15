from sqlalchemy import (
    Column,
    String,
    Numeric,
    ForeignKey,
    Integer,
    TIMESTAMP
)
import logging
from ether_sql.models import base

logger = logging.getLogger(__name__)


class StorageDiff(base):
    """
    Class mapping the storage_diff table in psql to difference in storage due to transactions
    """
    __tablename__ = 'storage_diff'
    id = Column(Integer, primary_key=True)
    block_number = Column(Numeric, ForeignKey('blocks.block_number'))
    timestamp = Column(TIMESTAMP)
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash'),
                              index=True)
    transaction_index = Column(Numeric, nullable=True)
    state_diff_id = Column(Integer, ForeignKey('state_diff.id'), nullable=False)
    address = Column(String(42), index=True, nullable=False)
    position = Column(String(66), nullable=False)
    storage_from = Column(String(66), nullable=True)
    storage_to = Column(String(66), nullable=True)

    def to_dict(self):
        return {
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'transaction_hash': self.transaction_hash,
            'transaction_index': self.transaction_index,
            'state_diff_id': self.state_diff_id,
            'address': self.address,
            'position': self.position,
            'storage_from': self.storage_from,
            'storage_to': self.storage_to,
        }

    @classmethod
    def add_storage_diff(cls, storage_diff_row, position, address,
                         transaction_hash, transaction_index, block_number,
                         timestamp, state_diff_id):

        assert isinstance(storage_diff_row, dict)
        key = list(storage_diff_row)
        if key[0] == '*':
            storage_from = storage_diff_row['*']['from'],
            storage_to = storage_diff_row['*']['to']
        elif key[0] == '+':
            storage_from = None
            storage_to = storage_diff_row['+']
        elif key[0] == '-':
            storage_from = storage_diff_row['-']
            storage_to = None
        else:
            raise ValueError('Unknown key {}'.format(key))

        storage_diff = cls(block_number=block_number,
                           timestamp=timestamp,
                           transaction_hash=transaction_hash,
                           transaction_index=transaction_index,
                           address=address,
                           position=position,
                           state_diff_id=state_diff_id,
                           storage_from=storage_from,
                           storage_to=storage_to)
        return storage_diff

    @classmethod
    def add_storage_diff_dict(cls, current_session, storage_diff_dict, address,
                              transaction_hash, transaction_index, block_number,
                              timestamp, state_diff_id):
        assert isinstance(storage_diff_dict, dict)
        for position in storage_diff_dict:
            storage_diff = cls.add_storage_diff(storage_diff_row=storage_diff_dict[position],
                                                position=position,
                                                address=address,
                                                state_diff_id=state_diff_id,
                                                transaction_hash=transaction_hash,
                                                transaction_index=transaction_index,
                                                block_number=block_number,
                                                timestamp=timestamp)
            current_session.db_session.add(storage_diff)
