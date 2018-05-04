from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy import LargeBinary, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db = declarative_base()


class Blocks(db):
    """
    Class defining a block in ethereum blockchain, its properties are more
    clearly defined in the ethereum yellow paper.

    :param int block_number: Quantity equal to number of blocks behind the current block
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
    transactions = relationship('Transactions', backref='block')
    uncles = relationship('Uncles', backref='block')
    uncle_count = Column(Integer, nullable=False)
    transaction_count = Column(Integer, nullable=False)

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


class Transactions(db):
    __tablename__ = 'transactions'
    transaction_hash = Column(String(66), primary_key=True)
    block_number = Column(Integer, ForeignKey('blocks.block_number'))
    nonce = Column(Integer, nullable=False)
    sender = Column(String(42), nullable=False)
    receiver = Column(String(42))
    start_gas = Column(Integer, nullable=False)
    value_szabo = Column(BigInteger, nullable=False)
    data = Column(LargeBinary)
    gas_price = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, ForeignKey('blocks.timestamp'))
    transaction_index = Column(Integer, nullable=False)

    def to_dict(self):
        return {
                'block_number': self.block_number,
                'transaction_hash': self.transaction_hash,
                'nonce': self.nonce,
                'sender': self.sender,
                'start_gas': self.start_gas,
                'value_szabo': self.value_szabo,
                'receiver': self.receiver,
                'data': self.data,
                'gas_price': self.gas_price,
                'timestamp': self.timestamp,
                'transaction_index': self.transaction_index}

    def __repr__(self):
        return "<Transaction {}>".format(self.transaction_hash)


class Uncles(db):
    __tablename__ = 'uncles'

    uncle_hash = Column(String(66), primary_key=True, unique=True)
    uncle_blocknumber = Column(Integer, nullable=False)
    parent_hash = Column(String(66), nullable=False)
    difficulty = Column(String(66), unique=True, nullable=False)
    current_blocknumber = Column(Integer, unique=True, index=True)
    gas_used = Column(Integer, nullable=False)
    miner = Column(String(42), nullable=False)
    timestamp = Column(TIMESTAMP, ForeignKey('blocks.timestamp'))
    sha3uncles = Column(String(66), nullable=False)
    extra_data = Column(LargeBinary)
    gas_limit = Column(Integer, nullable=False)

    def to_dict(self):
        return {
                'uncle_hash': self.uncle_hash,
                'uncle_blocknumber': self.uncle_blocknumber,
                'parent_hash': self.parent_hash,
                'difficulty': self.difficulty,
                'current_blocknumber': self.current_blocknumber,
                'gas_used': self.gas_used,
                'miner': self.miner,
                'timestamp': self.timestamp,
                'sha3uncles': self.sha3uncles,
                'extra_data': self.extra_data,
                'gas_limit': self.gas_limit
                }

        def __repr__(self):
            return "<Uncle {}>".format(self.uncle_hash)

# class Receipts(db):
