import logging
from sqlalchemy import Column, Numeric, ForeignKey, Integer
from ether_sql.models import base
from ether_sql.globals import get_current_session

logger = logging.getLogger(__name__)


class MetaInfo(base):
    """
    Contains meta information such as last uploaded block or
    current state information. Basically can be used as a placeholder for
    storing information in the tables.

    :param int last_pushed_block: Block number of the last block in the database
    """

    __tablename__ = 'meta_info'
    id = Column(Integer, primary_key=True)
    last_pushed_block = Column(Numeric, ForeignKey('blocks.block_number'))
    current_state_block = Column(Numeric)

    def to_dict(self):
        return {
            'last_pushed_block': self.last_pushed_block,
            'current_state_block': self.current_state_block,
        }

    @classmethod
    def get_last_pushed_block(cls):
        current_session = get_current_session()
        with current_session.db_session_scope():
            return current_session.db_session.query(cls).first().\
                        last_pushed_block

    @classmethod
    def get_current_state_block(cls):
        current_session = get_current_session()
        with current_session.db_session_scope():
            return current_session.db_session.query(cls).first().\
                        current_state_block

    @classmethod
    def set_last_pushed_block(cls, block_number):
        current_session = get_current_session()
        with current_session.db_session_scope():
            meta_info = current_session.db_session.query(cls).first()
            meta_info.last_pushed_block = block_number
            current_session.db_session.add(meta_info)

    @classmethod
    def set_current_state_block(cls, block_number):
        current_session = get_current_session()
        with current_session.db_session_scope():
            meta_info = current_session.db_session.query(cls).first()
            meta_info.current_state_block = block_number
            current_session.db_session.add(meta_info)
