from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from ether_sql.models import base


class Receipts(base):
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
