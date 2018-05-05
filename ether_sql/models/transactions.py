from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy import LargeBinary, BigInteger
from sqlalchemy.orm import relationship

from ether_sql.models import base


class Transactions(base):
    """
    Class defining a transaction in the ethereum blockchain, its properties are more
    accurately defined in the ethereum yellow paper https://github.com/ethereum/yellowpaper.

    :param str transaction_hash: The Keccak 256-bit hash of this transaction
    :param int block_number: Number of the block containing this transaction
    :param int nonce: Number of transactions sent by this sender
    :param str sender: Address of account which initiated this transaction
    :param int start_gas: Maximum amount of gas to be used while executing this transaction
    :param int value_wei: Number of wei to be transferred to the receiver of this transaction
    :param str receiver: Address of the recepient of this transaction, null if transaction creates a smart-contract
    :param bytes data: Unlimited size text specifying input data of message call or code of a contract create
    :param int gas_price: Number of wei to pay the miner per unit of gas
    :param int timestamp: Unix time at the at this transactions blocks
    :param int transaction_index: Position of this transaction in the transaction list of this block

    """
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
