from sqlalchemy import (
    Column,
    String,
    Numeric,
    Text,
    Integer,
)
import logging
from sqlalchemy.orm import relationship
from sqlalchemy import func, desc, or_
from ether_sql.models import base
from ether_sql.globals import get_current_session
from ether_sql.models import (
    Blocks,
    StateDiff,
    MetaInfo,
)
from ether_sql.models.storage import Storage
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
    def add_state(cls, address, balance, nonce, code):
        if nonce is None:
            _nonce = 0
        else:
            _nonce = nonce
        state = cls(
                    address=to_checksum_address(address),
                    balance=balance,
                    nonce=_nonce,
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
            current_session.db_session.query(Storage).delete()
            current_session.db_session.query(cls).delete()
            # query to get the balance
            query_balance = current_session.db_session.query(
                            StateDiff.address,
                            func.sum(StateDiff.balance_diff).label('balance'),
                            func.sum(StateDiff.nonce_diff).label('nonce')).\
                filter(StateDiff.block_number <= block_number).\
                group_by(StateDiff.address)
            subquery_balance = query_balance.subquery()
            # query to get the code
            row_number_column = func.row_number().over(
                partition_by=StateDiff.address,
                order_by=[StateDiff.block_number.desc(),
                          StateDiff.transaction_index.desc()])\
                .label('row_number')
            query_code = current_session.db_session.query(
                StateDiff.address.label('address'),
                StateDiff.code_to.label('code'))
            query_code = query_code.add_column(row_number_column)
            query_code = query_code.filter(
                or_(StateDiff.code_from != None, StateDiff.code_to != None))
            query_code = query_code.filter(StateDiff.block_number <= block_number)
            query_code = query_code.from_self().filter(row_number_column == 1)
            query_code = query_code.filter(StateDiff.code_to != '0x')
            subquery_code = query_code.subquery()
            # joining the two queries
            query_state = current_session.db_session.query(
                subquery_balance.c.address,
                subquery_balance.c.balance,
                subquery_balance.c.nonce,
                subquery_code.c.code)
            query_state = query_state.outerjoin(subquery_code, subquery_balance.c.address == subquery_code.c.address)

            # updating the state table with query results
            for row in query_state:
                state = cls.add_state(
                    address=row.address,
                    balance=row.balance,
                    nonce=row.nonce,
                    code=row.code)
                current_session.db_session.add(state)
            # update the meta_info.current_state_block
            MetaInfo.set_current_state_block(current_session, block_number)

        with current_session.db_session_scope():
            # update the storage table
            Storage.get_storage_at_block(current_session, block_number)
