import logging
from sqlalchemy import Column, String, Numeric, TIMESTAMP, Text, Integer
from sqlalchemy import func
from web3.utils.encoding import (to_int, to_hex)
from eth_utils import to_checksum_address
from ether_sql.models import base
from ether_sql.globals import get_current_session
logger = logging.getLogger(__name__)

class BlockTaskMeta(base):
    """
    Class mapping success or failure of block scrapper tasks.

    """
    __tablename__ = 'block_task_meta'
    id = Column(Integer, primary_key=True)
    task_id = Column(Text, nullable=False)
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
    def get_task_from_id(cls, task_id):
        current_session = get_current_session()
        with current_session.db_session_scope():
            return current_session.db_session.query(cls).\
                    filter_by(task_id=task_id).first()
