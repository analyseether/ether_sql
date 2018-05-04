from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy import LargeBinary, BigInteger, Boolean
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
    transaction_hash = Column(String(66), primary_key=True, index=True)
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
    logs = relationship('Logs', backref='receipt')
    traces = relationship('Traces', backref='traces')

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

    uncle_hash = Column(String(66), primary_key=True, unique=True, index=True)
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


class Receipts(db):
    __tablename__ = 'receipts'

    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash'),
                              primary_key=True, index=True)
    status = Column(Boolean, nullable=True)
    gas_used = Column(Integer, nullable=False)
    cumulative_gas_used = Column(Integer, nullable=False)
    contract_address = Column(String(42))
    block_number = Column(Integer, ForeignKey('blocks.block_number'))
    timestamp = Column(TIMESTAMP, ForeignKey('blocks.timestamp'))
    transaction_index = Column(Integer, nullable=False)
    logs = relationship('Logs', backref='receipt')
    traces = relationship('Traces', backref='traces')

    def to_dict(self):
        return {
            'transaction_hash': self.transaction_hash,
            'status': self.status,
            'gas_used': self.gas_used,
            'cumulative_gas_used': self.cumulative_gas_used,
            'contract_address': self.contract_address,
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'transaction_index': self.transaction_index
            }

    def __repr__(self):
        return "<Receipt {}>".format(self.transaction_hash)


class Logs(db):
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


class Traces(db):
    __tablename__ = 'traces'
    id = Column(Integer, primary_key=True)
    block_number = Column(Integer, ForeignKey('blocks.block_number'))
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash'),
                              index=True)
    trace_type = Column(String, nullable=False)
    trace_address = Column(String, nullable=False)
    subtraces = Column(Integer, nullable=True)
    transaction_index = Column(Integer, nullable=True)
    sender = Column(String(42), nullable=True)
    receiver = Column(String(42), nullable=True)
    value_wei = Column(BigInteger, nullable=True)
    start_gas = Column(Integer)
    input_data = Column(LargeBinary)
    gas_used = Column(Integer)
    contract_address = Column(String(42), nullable=True)
    output = Column(LargeBinary)
    error = Column(String(42))

    def to_dict(self):
        {
         'block_number': self.block_number,
         'transaction_hash': self.transaction_hash,
         'trace_type': self.trace_type,
         'trace_address': self.trace_address,
         'subtraces': self.subtraces,
         'transaction_index': self.transaction_index,
         'sender': self.sender,
         'receiver': self.receiver,
         'value_wei': self.value_wei,
         'start_gas': self.start_gas,
         'input_data': self.input_data,
         'gas_used': self.gas_used,
         'contract_address': self.contract_address,
         'output': self.output,
         'error': self.error
        }
