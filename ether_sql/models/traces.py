from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import LargeBinary, BigInteger

from ether_sql.models import base


class Traces(base):
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
