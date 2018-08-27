import logging
from sqlalchemy import (
    Column,
    String,
    Numeric,
    Integer,
    ForeignKey,
)
from web3.utils.formatters import hex_to_integer
from ether_sql.models import base
from ether_sql.globals import get_current_session
from ether_sql.models import StorageDiff
from sqlalchemy import func, desc, and_

logger = logging.getLogger(__name__)


class Storage(base):
    """
    Class mapping the current storage of the ethereum blockchain to the
    storage table in psql

    :param str address: Account address which has this state
    :param str position: The balance of the account
    :param str Storage: Value of storage
    """
    __tablename__ = 'storage'
    id = Column(Integer, primary_key=True)
    address = Column(String(42), ForeignKey('state.address', ondelete='CASCADE'))
    position = Column(String(66), index=True, nullable=False)
    storage = Column(String(66), nullable=False)

    def to_dict(self):
        return {
            'address': self.address,
            'position': self.position,
            'storage': self.storage}

    @classmethod
    def add_storage(cls, address, position, storage):
        storage = cls(address=address, position=position, storage=storage)
        return storage

    @classmethod
    def get_storage_at_block(cls, current_session, block_number):
        """
        Gives the storage values at requested block

        :param int block_number: Block number of desired storage, always
        required since it is called from method `State.get_state_at_block`
        """
        row_number_column = func.row_number().over(
            partition_by=[StorageDiff.address, StorageDiff.position],
            order_by=[StorageDiff.block_number.desc(),
                      StorageDiff.transaction_index.desc()])\
            .label('row_number')
        query = current_session.db_session.query(StorageDiff.address, StorageDiff.position, StorageDiff.storage_to.label('storage'))
        query = query.add_column(row_number_column)
        query = query.filter(
            and_(
                StorageDiff.block_number <= block_number,
                StorageDiff.storage_to != '0x0000000000000000000000000000000000000000000000000000000000000000'))
        query = query.from_self().filter(row_number_column == 1)

        for row in query:
            if row.storage is not None:
                if hex_to_integer(row.storage) != 0:
                    storage = cls.add_storage(address=row.address, position=row.position, storage=row.storage)
                else:
                    # not adding storage positions where value is 0, since parity discards these positions during export
                    logger.debug('address: {}, position {}, storage: {} is zero'.format(row.address, row.position, row.storage))
                current_session.db_session.add(storage)
            else:
                logger.debug('address: {}, position {}, storage: {} is none'.format(row.address, row.position, row.storage))
