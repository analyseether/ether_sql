from sqlalchemy import Column, String, Integer, TIMESTAMP, LargeBinary
from sqlalchemy.orm import relationship

from ether_sql.models import base


class Blocks(base):
    """
    Class defining a block in the ethereum blockchain, its properties are more
    clearly defined in the ethereum yellow paper https://github.com/ethereum/yellowpaper.

    :param int block_number: Quantity equal to number of blocks behind the current block
    :param str block_hash: The Keccak 256-bit hash of this block
    :param str parent_hash: The Keccak 256-bit hash of the parent of this block
    :param int difficulty: Difficulty level of this block
    :param int gas_used: Total gas used by the transactions in this block
    :param str miner: Address to which all block rewards are transferred
    :param int timestamp: Unix time at the at this blocks inception
    :param str sha3uncles: Keccak 256-bit hash of the uncles portion of this block
    :param bytes extra_data: Byte array of 32 bytes or less containing extra data of this block
    :param int gas_limit: Current maximum gas expenditure per block
    :param int uncle_count: Number of uncles in this block
    :param int transaction_count': Number of transactions in this block

    """
    __tablename__ = 'blocks'
    block_number = Column(Integer, primary_key=True, index=True)
    block_hash = Column(String(66), unique=True, nullable=False)
    parent_hash = Column(String(66), unique=True, nullable=False)
    difficulty = Column(Integer, nullable=False)
    gas_used = Column(Integer, nullable=False)
    miner = Column(String(42), nullable=False)
    timestamp = Column(TIMESTAMP, unique=True, nullable=False)
    sha3uncles = Column(String(66), nullable=False)
    extra_data = Column(LargeBinary)
    gas_limit = Column(Integer, nullable=False)
    uncle_count = Column(Integer, nullable=False)
    transaction_count = Column(Integer, nullable=False)
    transactions = relationship('Transactions', backref='blocks')
    uncles = relationship('Uncles', backref='blocks')
    logs = relationship('Logs', backref='blocks')
    traces = relationship('Traces', backref='blocks')

    def to_dict(self):
        return {
            'block_number': self.block_number,
            'block_hash': self.block_hash,
            'parent_hash': self.parent_hash,
            'difficulty': self.difficulty,
            'gas_used': self.gas_used,
            'miner': self.miner,
            'timestamp': self.timestamp,
            'sha3uncles': self.sha3uncles,
            'extra_data': self.extra_data,
            'gas_limit': self.gas_limit,
            'uncle_count': self.uncle_count,
            'transaction_count': self.transaction_count
            }

    def __repr__(self):
        return "<Block {}>".format(self.block_number)
