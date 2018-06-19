import logging
from sqlalchemy import Column, Numeric, ForeignKey, Integer
from ether_sql.models import base


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
