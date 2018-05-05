from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy import LargeBinary, BigInteger
from sqlalchemy.orm import relationship

from ether_sql.models import base


class Transactions(base):
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
