import logging
from sqlalchemy import Column, String, Numeric, TIMESTAMP, Text, Integer
from sqlalchemy import func, and_
from web3.utils.encoding import (to_int, to_hex)
from eth_utils import to_checksum_address
from ether_sql.models import base
from ether_sql.globals import get_current_session
from web3.utils.encoding import to_int, to_hex
logger = logging.getLogger(__name__)

class BlockTaskMeta(base):
    """
    Class mapping success or failure of block scrapper tasks.

    """
    __tablename__ = 'block_task_meta'
    id = Column(Integer, primary_key=True)
    task_id = Column(Text, nullable=True)
    task_name = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    block_number = Column(Numeric, nullable=False)
    block_hash = Column(String(66), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'task_name': self.task_name,
            'state': self.state,
            'block_number': self.block_number,
            'block_hash': self.block_hash,
            }

    @classmethod
    def add_block_task_meta(cls, block_number, task_name, state, task_id=None, block_hash=None):
        current_session = get_current_session()
        block_task_meta = cls(task_name=task_name,
                              state=state,
                              block_number=block_number,
                              block_hash=block_hash,
                              task_id=task_id)
        with current_session.db_session_scope():
            current_session.db_session.add(block_task_meta)

    @classmethod
    def update_block_task_meta_from_block_number(cls, current_session,
            block_number, **kwargs):
        block_task_meta = current_session.db_session.query(cls).\
                filter_by(block_number=block_number)
        logger.debug('Updating task meta of block {0}'.format(block_number))
        for i_block_task_meta in block_task_meta:
            for key, value in kwargs.items():
                setattr(i_block_task_meta, key, value)
                current_session.db_session.add(i_block_task_meta)
            logger.debug('Updated task meta {}'.format(i_block_task_meta.to_dict()))

    @classmethod
    def get_block_task_meta_from_task_id(cls, current_session, task_id):
        return current_session.db_session.query(cls).\
            filter_by(task_id=task_id)

    @classmethod
    def get_block_task_meta_from_block_number(cls, current_session, block_number):
        return current_session.db_session.query(cls).\
            filter_by(block_number=block_number)

    @classmethod
    def get_block_task_meta_from_block_hash(cls, current_session, block_hash):
        return current_session.db_session.query(cls).\
            filter_by(block_hash=block_hash)

    @classmethod
    def get_blocks_to_be_pushed_in_queue(cls, current_session):
        current_session = get_current_session()
        current_eth_blocknumber = current_session.w3.eth.blockNumber
        block_lag = current_session.settings.BLOCK_LAG
        query = current_session.db_session.query(cls.block_number).filter(
            and_(cls.state=='WAITING',
            cls.block_number < current_eth_blocknumber-block_lag))
        return query.from_self().distinct()
