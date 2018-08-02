from sqlalchemy import Column, String, Numeric, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
import logging
from web3.utils.encoding import to_int, to_hex
from eth_utils import to_checksum_address
from ether_sql.models import base

logger = logging.getLogger(__name__)


class Transactions(base):
    """
    Class mapping a transaction table in the psql database to a transaction in ethereum node.

    :param str transaction_hash: The Keccak 256-bit hash of this transaction
    :param int block_number: Number of the block containing this transaction
    :param int nonce: Number of transactions sent by this sender
    :param str sender: Address of account which initiated this transaction
    :param int start_gas: Maximum amount of gas to be used while executing this transaction
    :param int value_wei: Number of wei to be transferred to the receiver of this transaction
    :param str receiver: Address of the recepient of this transaction, null if transaction creates a smart-contract
    :param str data: Unlimited size text specifying input data of message call or code of a contract create
    :param int gas_price: Number of wei to pay the miner per unit of gas
    :param int timestamp: Unix time at the at this transactions blocks
    :param datetime transaction_index: Position of this transaction in the transaction list of this block

    """
    __tablename__ = 'transactions'
    transaction_hash = Column(String(66), primary_key=True, index=True)
    block_number = Column(Numeric, ForeignKey('blocks.block_number', ondelete='CASCADE'))
    nonce = Column(Numeric, nullable=False)
    sender = Column(String(42), nullable=False)
    receiver = Column(String(42))
    start_gas = Column(Numeric, nullable=False)
    value = Column(Numeric)
    data = Column(Text)
    gas_price = Column(Numeric, nullable=False)
    timestamp = Column(TIMESTAMP)
    transaction_index = Column(Numeric, nullable=False)
    receipt = relationship('Receipts', backref='transactions')
    logs = relationship('Logs', backref='transactions')
    traces = relationship('Traces', backref='transactions')
    state_diff = relationship('StateDiff', backref='transactions')

    def to_dict(self):
        return {
                'block_number': self.block_number,
                'transaction_hash': self.transaction_hash,
                'nonce': self.nonce,
                'sender': self.sender,
                'start_gas': self.start_gas,
                'value': self.value,
                'receiver': self.receiver,
                'data': self.data,
                'gas_price': self.gas_price,
                'timestamp': self.timestamp,
                'transaction_index': self.transaction_index}

    def __repr__(self):
        return "<Transaction {}>".format(self.transaction_hash)

    @classmethod
    def add_transaction(cls, transaction_data, block_number, iso_timestamp):
        """
        Creates a new transaction object from data received from JSON-RPC call
        eth_getBlockByNumber.

        :param dict transaction_data: data received from JSON RPC call
        :param datetime iso_timestamp: timestamp when the block containing the transaction was mined
        :param int block_number: block number of the block where this transaction was included
        """
        try:
            receiver = to_checksum_address(transaction_data['to'])
        except TypeError:
            receiver = None

        transaction = cls(block_number=block_number,
                          nonce=to_int(transaction_data['nonce']),
                          transaction_hash=to_hex(transaction_data['hash']),
                          sender=to_checksum_address(transaction_data['from']),
                          start_gas=to_int(transaction_data['gas']),
                          value=int(str(to_int(transaction_data['value']))),
                          receiver=receiver,
                          data=transaction_data['input'],
                          gas_price=str(to_int(transaction_data['gasPrice'])),
                          timestamp=iso_timestamp,
                          transaction_index=to_int(transaction_data['transactionIndex']))

        return transaction
