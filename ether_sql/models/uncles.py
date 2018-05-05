from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy import LargeBinary


from ether_sql.models import base


class Uncles(base):
    __tablename__ = 'uncles'

    uncle_hash = Column(String(66), primary_key=True, unique=True, index=True)
    uncle_blocknumber = Column(Integer, nullable=False)
    parent_hash = Column(String(66), nullable=False)
    difficulty = Column(String(66), unique=True, nullable=False)
    current_blocknumber = Column(Integer, unique=True, index=True)
    gas_used = Column(Integer, nullable=False)
    miner = Column(String(42), nullable=False)
    timestamp = Column(TIMESTAMP, ForeignKey('blocks.timestamp'))
    sha3uncles = Column(String(66), nullable=False)
    extra_data = Column(LargeBinary)
    gas_limit = Column(Integer, nullable=False)

    def to_dict(self):
        return {
                'uncle_hash': self.uncle_hash,
                'uncle_blocknumber': self.uncle_blocknumber,
                'parent_hash': self.parent_hash,
                'difficulty': self.difficulty,
                'current_blocknumber': self.current_blocknumber,
                'gas_used': self.gas_used,
                'miner': self.miner,
                'timestamp': self.timestamp,
                'sha3uncles': self.sha3uncles,
                'extra_data': self.extra_data,
                'gas_limit': self.gas_limit
                }

    def __repr__(self):
        return "<Uncle {}>".format(self.uncle_hash)
