from sqlalchemy import Column, String, Numeric, ForeignKey, Text, Integer
import logging
from web3.utils.encoding import to_hex
from web3.utils.formatters import hex_to_integer
from eth_utils import to_checksum_address
from ether_sql.models import base


logger = logging.getLogger(__name__)


class Traces(base):
    """
    Class mapping a traces table in the psql database to a trace in ethereum node.

    :param int block_number: Number of the block containing this trace
    :param str transaction_hash: The of the transaction containing this trace
    :param str trace_type: Type of trace available types; 'call', 'create', 'suicide' and 'reward'
    :param str trace_address: Array of integers specifying the address of the trace in this transaction
    :param int subtraces: Number of subsequent traces
    :param int transaction_index: Position of the transaction in this block
    :param str sender: Address of account which initiated this trace
    :param str receiver: Address of recepient of this trace, null for trace_type = 'create' or 'suicide'
    :param int value: Number of wei to be transferred to the receiver of this trace
    :param int start_gas: Maximum amount of gas to be used while executing this trace
    :param str input_data: Unlimited size text specifying input data of message call or code of a contract create
    :param int gas_used: The amount of gas utilized by this step
    :param str contract_address: Address of created contract if trace_type = 'create' else null
    :param str output: Output of this trace
    :param str error: Error message if this step resulted in an error

    .. note::

        This needs proper `documentation <https://ethereum.stackexchange.com/questions/31443/what-do-the-response-values-of-a-parity-trace-transaction-call-actually-repres>`_ from team parity

    """

    __tablename__ = 'traces'
    id = Column(Integer, primary_key=True)
    block_number = Column(Numeric, ForeignKey('blocks.block_number', ondelete='CASCADE'))
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash', ondelete='CASCADE'),
                              index=True)
    trace_type = Column(String, nullable=False)
    trace_address = Column(String, nullable=False)
    subtraces = Column(Numeric, nullable=True)
    transaction_index = Column(Numeric, nullable=True)
    sender = Column(String(42), nullable=True)
    receiver = Column(String(42), nullable=True)
    value = Column(Numeric, nullable=True)
    start_gas = Column(Numeric)
    input_data = Column(Text)
    gas_used = Column(Numeric)
    contract_address = Column(String(42), nullable=True)
    output = Column(Text)
    error = Column(String(42))

    def to_dict(self):
        return {
         'block_number': self.block_number,
         'transaction_hash': self.transaction_hash,
         'trace_type': self.trace_type,
         'trace_address': self.trace_address,
         'subtraces': self.subtraces,
         'transaction_index': self.transaction_index,
         'sender': self.sender,
         'receiver': self.receiver,
         'value': self.value,
         'start_gas': self.start_gas,
         'input_data': self.input_data,
         'gas_used': self.gas_used,
         'contract_address': self.contract_address,
         'output': self.output,
         'error': self.error
        }

    @classmethod
    def add_trace(cls, dict_trace, transaction_hash, transaction_index,
                  block_number, timestamp):
        """
        Creates a new trace object from data received from JSON-RPC call
        trace_transaction.

        :param dict dict_trace: trace data received from the JSON RPC callable
        :param int timestamp: timestamp of the block where this trace was included
        :param int block_number: block number of the block where this trance was included

        """
        logger.debug(dict_trace['action'])
        trace = cls(transaction_hash=transaction_hash,
                    block_number=block_number,
                    trace_address=dict_trace['traceAddress'],
                    subtraces=dict_trace['subtraces'],
                    transaction_index=transaction_index,
                    trace_type=dict_trace['type'],
                    sender='',
                    receiver='',
                    start_gas=None,
                    value=None,
                    input_data='',
                    gas_used=None,
                    output='',
                    contract_address='',
                    error='')

        action = dict_trace['action']

        if trace.trace_type == 'call':
            # parsing action
            trace.sender = to_checksum_address(action['from'])
            trace.receiver = to_checksum_address(action['to'])
            trace.start_gas = hex_to_integer(action['gas'])
            trace.value = hex_to_integer(action['value'])
            trace.input_data = action['input']
            # parsing result
            if 'result' in list(dict_trace.keys()):
                result = dict_trace['result']
                trace.gas_used = hex_to_integer(result['gasUsed'])
                trace.output = result['output']
            else:
                trace.error = dict_trace['error']
        elif trace.trace_type == 'create':
            logger.debug('Type {}, action {}'.format(dict_trace['type'], action))
            # parsing action
            trace.start_gas = hex_to_integer(action['gas'])
            trace.value = hex_to_integer(action['value'])
            trace.input_data = action['init']
            # parsing result
            if 'result' in list(dict_trace.keys()):
                result = dict_trace['result']
                trace.gas_used = hex_to_integer(result['gasUsed'])
                trace.output = result['code']
                trace.contract_address = to_checksum_address(result['address'])
            else:
                trace.error = dict_trace['error']
        elif trace.trace_type == 'suicide':
            logger.debug('Type {}, action {}'.format(dict_trace['type'], action))
            # parsing action
            trace.sender = to_checksum_address(action['address'])
            trace.receiver = to_checksum_address(action['refundAddress'])
            trace.value = hex_to_integer(action['balance'])
            # parsing result
            logger.debug('Type encountered {}'.format(dict_trace['type']))

        return trace

    @classmethod
    def add_trace_list(cls, current_session, trace_list, transaction_hash,
                       transaction_index, block_number, timestamp):
        """
        Adds a list of traces in the sql session
        """
        for dict_trace in trace_list:
            trace = cls.add_trace(dict_trace,
                                  transaction_hash=transaction_hash,
                                  transaction_index=transaction_index,
                                  block_number=block_number,
                                  timestamp=timestamp)
        # added the trace in the db session
        current_session.db_session.add(trace)
