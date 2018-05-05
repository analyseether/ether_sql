from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from ether_sql.models import base


class Receipts(base):
    """
    Class defining a receipt in the ethereum blockchain, its properties are more
    clearly defined in the ethereum yellow paper https://github.com/ethereum/yellowpaper.

    :param str transaction_hash: The Keccak 256-bit hash of this transaction
    :param bool status: Success or failure of this transaction, included after the Byzantinium fork
    :param int gas_used: Amount of gas used by this specific transaction alone
    :param int cumulative_gas_used: Total amount of gas used after this transaction was included in the block
    :param str contract_address: Contract address create if transaction was a contract create transaction, else null
    :param int block_number: Number of the block containing this transaction
    :param int timestamp: Unix time at the at this transactions blocks
    :param int transaction_index: Position of this transaction in the transaction list of this block
    """
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
