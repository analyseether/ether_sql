from sqlalchemy import (
    Column,
    String,
    Numeric,
    Integer,
    ForeignKey,
)
from ether_sql.models import base


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
    address = Column(String(42), ForeignKey('state.address'))
    position = Column(String(66), index=True, nullable=False)
    storage = Column(String(66), nullable=False)
