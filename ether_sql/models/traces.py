from sqlalchemy import Column, String, Numeric, ForeignKey, Text, Integer
from ethereum import utils
import logging

from ether_sql.models import base


logger = logging.getLogger(__name__)


class Traces(base):
    __tablename__ = 'traces'
    id = Column(Integer, primary_key=True)
    block_number = Column(Numeric, ForeignKey('blocks.block_number'))
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash'),
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
        {
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
    def add_trace(cls, dict_trace, block_number, timestamp):
        """

        """
        trace = cls(transaction_hash=dict_trace['transactionHash'],
                    block_number=dict_trace['blockNumber'],
                    trace_address=dict_trace['traceAddress'],
                    subtraces=dict_trace['subtraces'],
                    transaction_index=dict_trace['transactionPosition'],
                    trace_type=dict_trace['type'],
                    sender='',
                    receiver='',
                    start_gas='',
                    value=None,
                    input_data='',
                    gas_used='',
                    output='',
                    contract_address='',
                    error='')

        action = dict_trace['action']

        if trace.trace_type == 'call':
            # parsing action
            trace.sender = action['from']
            trace.receiver = action['to']
            trace.start_gas = utils.parse_int_or_hex(action['gas'])
            trace.value = utils.parse_int_or_hex(action['value'])
            trace.input_data = action['input']
            # parsing result
            if 'result' in dict_trace.keys():
                result = dict_trace['result']
                trace.gas_used = utils.parse_int_or_hex(result['gasUsed'])
                trace.output = result['output']
            else:
                trace.error = dict_trace['error']
        elif trace.trace_type == 'create':
            logger.debug('Type {}, action {}'.format(dict_trace['type'], action))
            # parsing action
            trace.start_gas = utils.parse_int_or_hex(action['gas'])
            trace.value = utils.parse_int_or_hex(action['value'])
            trace.input_data = action['init']
            # parsing result
            if 'result' in dict_trace.keys():
                result = dict_trace['result']
                trace.gas_used = utils.parse_int_or_hex(result['gasUsed'])
                trace.output = result['code']
                trace.contract_address = result['address']
            else:
                trace.error = dict_trace['error']
        elif trace.trace_type == 'suicide':
            logger.debug('Type {}, action {}'.format(dict_trace['type'], action))
            # parsing action
            trace.sender = action['address']
            trace.receiver = action['refundAddress']
            trace.value = utils.parse_int_or_hex(action['balance'])
            # parsing result
            logger.debug('Type encountered {}'.format(dict_trace['type']))

        return trace
