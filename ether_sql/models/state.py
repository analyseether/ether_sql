from sqlalchemy import (
    Column,
    String,
    Numeric,
    Text,
    Integer,
)
import logging
from sqlalchemy.orm import relationship
from sqlalchemy import func
from ether_sql.models import base
from ether_sql.globals import get_current_session
from ether_sql.models import (
    Blocks,
    StateDiff,
    MetaInfo,
)
from ether_sql.exceptions import MissingBlocksError
from eth_utils import to_checksum_address

logger = logging.getLogger(__name__)


class State(base):
    """
    Class mapping a state table in psql to the state of ethereum blockchain

    :param str address: Account address which has this state
    :param int balance: The balance of the account
    :param int nonce: The Nonce of the account
    :param str code: The code of this account
    """
    __tablename__ = 'state'
    address = Column(String(42), primary_key=True, index=True)
    balance = Column(Numeric, nullable=False)
    nonce = Column(Integer, nullable=True)
    code = Column(Text, nullable=True)
    storage = relationship('Storage', backref='state')

    def to_dict(self):
        return {
            'address': self.address,
            'balance': self.balance,
            'nonce': self.balance,
            'code': self.code
        }

    @classmethod
    def add_state(cls, address, balance, nonce, code=None):
        state = cls(
                    address=to_checksum_address(address),
                    balance=balance,
                    nonce=nonce,
                    code=code)
        return state

    @classmethod
    def get_state_at_block(cls, block_number=None):
        """
        Updates the state with either specified `block_number` or the maximum
        ``block_number`` in the database. Also, checks if there are any missing
        blocks in the database, if yes then stops the calculation of state
        prematurely.

        : param int block_number: Block number of desired state, if none then
        constructs the state for the highest available state_diff
        """
        # checks if there are any gaps in the block_numbers
        if block_number is None:
            block_number = Blocks.get_max_block_number()

        missing_block_numbers = Blocks.missing_blocks(block_number)
        if len(missing_block_numbers) > 0:
            raise MissingBlocksError('Cannot construct state at block {}, \
                    {} blocks are missing'.format(block_number,
                                                  len(missing_block_numbers)))

        if MetaInfo.get_current_state_block == block_number:
            logger.info('State is already at block {}'.format(block_number))
            return

        current_session = get_current_session()
        with current_session.db_session_scope():
            # Removing the contents of state if meta_info.current_state_block != block_number
            current_session.db_session.query(cls).delete()
            # query to get the state at block_number
            query = current_session.db_session.query(
                        StateDiff.address,
                        func.sum(StateDiff.balance_diff).label('balance'),
                        func.sum(StateDiff.nonce_diff).label('nonce')).\
                filter(StateDiff.block_number <= block_number).\
                group_by(StateDiff.address)
            # updating the state table with query results
            for row in query:
                if row.nonce is None:
                    nonce = 0
                else:
                    nonce = row.nonce
                state = cls(
                    address=row.address,
                    balance=row.balance,
                    nonce=nonce,
                    code=None)
                current_session.db_session.add(state)
        # update the meta_info.current_state_block
        MetaInfo.set_current_state_block(block_number)
