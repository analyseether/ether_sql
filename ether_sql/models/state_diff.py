from sqlalchemy import (
    Column,
    String,
    Numeric,
    ForeignKey,
    Text,
    Integer,
    TIMESTAMP
)
from sqlalchemy.orm import relationship
import logging
import decimal
import csv
from web3.utils.formatters import hex_to_integer
from ether_sql.models import base
from ether_sql.models.storage_diff import StorageDiff
from ether_sql.models.transactions import Transactions
from ether_sql.models.blocks import Blocks
from ether_sql.constants.mainnet import (
    FORK_BLOCK_NUMBER,
    PRE_BYZANTINIUM_REWARD,
    POST_BYZANTINIUM_REWARD,
)
from eth_utils import to_checksum_address
logger = logging.getLogger(__name__)


class StateDiff(base):
    """
    Class mapping a state_diff table in psql to a difference in state after transactions

    :param int block_number: Number of the block containing this StateDiff
    :param timestamp timestamp: Unix time at the mining of this block
    :param str transaction_hash: The transaction hash if this was created by a transaction
    :param int transaction_index: Position of this transaction in the transaction list of the block
    :param str address: Account address where the change occoured
    :param int balance_diff: Difference in balance due to this row
    :param int nonce_diff: Difference in nonce due to this row
    :param str code_from: Initial code of this account
    :param str code_to: Final code of this account
    """

    __tablename__ = 'state_diff'
    id = Column(Integer, primary_key=True, autoincrement=True)
    block_number = Column(Numeric, ForeignKey('blocks.block_number', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP)
    # nullable because some state changes also occour because of miner rewards
    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash', ondelete='CASCADE'),
                              nullable=True,
                              index=True)
    transaction_index = Column(Numeric, nullable=True)
    address = Column(String(42), index=True, nullable=False)
    balance_diff = Column(Numeric, nullable=True)
    nonce_diff = Column(Integer, nullable=True)
    code_from = Column(Text, nullable=True)
    code_to = Column(Text, nullable=True)
    state_diff_type = Column(String(10))
    storage_diff = relationship('StorageDiff', backref='state_diff')

    def to_dict(self):
        return {
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'transaction_hash': self.transaction_hash,
            'transaction_index': self.transaction_index,
            'address': self.address,
            'balance_diff': self.balance_diff,
            'nonce_diff': self.nonce_diff,
            'code_from': self.code_from,
            'code_to': self.code_to,
            'state_diff_type': self.state_diff_type,
        }

    def _parseStateDiff(account_state, type):
        state_from = None
        state_to = None
        state_diff = None

        assert len(account_state) == 1
        if isinstance(account_state, dict):
            key = list(account_state)
            if key[0] == '*':
                if type == 'code':
                    state_from = account_state['*']['from']
                    state_to = account_state['*']['to']
                else:
                    state_diff = hex_to_integer(account_state['*']['to']) - \
                                 hex_to_integer(account_state['*']['from'])
            elif key[0] == '+':
                if type == 'code':
                    state_to = account_state['+']
                else:
                    state_diff = hex_to_integer(account_state['+'])
            elif key[0] == '-':
                if type == 'code':
                    state_from = account_state['-']
                else:
                    state_diff = -1*hex_to_integer(account_state['-'])
            else:
                raise ValueError('Unknown key {} in account state'.format(key))
        elif account_state == '=':
            logger.debug('No change in type'.format(type))
        else:
            raise ValueError('Unknown account state {}'.format(account_state))
        return state_from, state_to, state_diff

    @classmethod
    def add_state_diff(cls, balance_diff, nonce_diff, code_from, code_to,
                       address, transaction_hash, transaction_index,
                       block_number, timestamp, miner=None, fees=None,
                       state_diff_type=None):
        """
        Creates a new state_diff object
        """
        address = to_checksum_address(address)

        if nonce_diff == +1:
            state_diff_type = 'sender'
        if miner is not None:
            if address == miner and balance_diff == fees:
                state_diff_type = 'fees'

        state_diff = cls(block_number=block_number,
                         timestamp=timestamp,
                         transaction_hash=transaction_hash,
                         transaction_index=transaction_index,
                         address=address,
                         balance_diff=balance_diff,
                         nonce_diff=nonce_diff,
                         code_from=code_from,
                         code_to=code_to,
                         state_diff_type=state_diff_type)
        return state_diff

    @classmethod
    def add_state_diff_dict(cls, current_session, state_diff_dict,
                            transaction_hash, transaction_index, block_number,
                            timestamp, miner, fees):
        """
        Creates a bunch of state_diff objects upon receiving them as a
        dictionary and adds them to the current db_session
        """
        for address in state_diff_dict:
            balance_from, balance_to, balance_diff = cls._parseStateDiff(
                state_diff_dict[address]['balance'], 'balance')
            nonce_from, nonce_to, nonce_diff = cls._parseStateDiff(
                state_diff_dict[address]['nonce'], 'nonce')
            code_from, code_to, code_diff = cls._parseStateDiff(
                state_diff_dict[address]['code'], 'code')

            state_diff = cls.add_state_diff(
                            balance_diff=balance_diff,
                            nonce_diff=nonce_diff,
                            code_from=code_from,
                            code_to=code_to,
                            address=address,
                            transaction_hash=transaction_hash,
                            transaction_index=transaction_index,
                            block_number=block_number,
                            timestamp=timestamp,
                            miner=miner,
                            fees=fees)
            current_session.db_session.add(state_diff)

            if state_diff_dict[address]['storage'] is not {}:
                current_session.db_session.flush()
                StorageDiff.add_storage_diff_dict(
                        current_session=current_session,
                        storage_diff_dict=state_diff_dict[address]['storage'],
                        state_diff_id=state_diff.id,
                        address=address,
                        transaction_hash=transaction_hash,
                        transaction_index=transaction_index,
                        block_number=block_number,
                        timestamp=timestamp)

    @classmethod
    def add_mining_rewards(cls, current_session, block, uncle_list):
        """
        Adds the mining and uncle rewards to the state_diff table
        """
        miner_reward = PRE_BYZANTINIUM_REWARD
        if block.block_number > FORK_BLOCK_NUMBER['Byzantium']:
            miner_reward = POST_BYZANTINIUM_REWARD
        uncle_inclusion_reward = int(len(uncle_list)*miner_reward/32.0)
        # adding the miner reward
        state_diff = StateDiff.add_state_diff(
            balance_diff=miner_reward+uncle_inclusion_reward,
            nonce_diff=None,
            code_from=None,
            code_to=None,
            address=block.miner,
            transaction_hash=None,
            transaction_index=None,
            block_number=block.block_number,
            timestamp=block.timestamp,
            state_diff_type='miner'
            )
        current_session.db_session.add(state_diff)
        # adding the uncles
        for uncle in uncle_list:
            factor = (uncle.uncle_blocknumber + 8 - uncle.current_blocknumber)/8.0
            uncle_reward = int(factor*miner_reward)
            state_diff = StateDiff.add_state_diff(
                balance_diff=uncle_reward,
                nonce_diff=None,
                code_from=None,
                code_to=None,
                address=uncle.miner,
                transaction_hash=None,
                transaction_index=None,
                block_number=block.block_number,
                timestamp=block.timestamp,
                state_diff_type='uncle'
                )
            current_session.db_session.add(state_diff)

    @classmethod
    def parse_genesis_rewards(cls, current_session, block):
        with open('ether_sql/constants/genesis_rewards.csv',
                  'r', encoding='utf-8') as genesis_rewards:
            reader = csv.reader(genesis_rewards)
            for row in reader:
                state_diff = StateDiff.add_state_diff(
                                balance_diff=row[1],
                                nonce_diff=None,
                                code_from=None,
                                code_to=None,
                                address=row[0],
                                transaction_hash=None,
                                transaction_index=None,
                                block_number=block.block_number,
                                timestamp=block.timestamp,
                                state_diff_type='genesis')

                current_session.db_session.add(state_diff)
