from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


db = declarative_base()

class Blocks(db):
    __tablename__ = 'blocks'
    block_number = Column(Integer, primary_key=True)
    block_hash = Column(String(66), unique=True, nullable=False)
    parent_hash = Column(String(66), unique=True, nullable=False)
    difficulty = Column(Integer, nullable=False)
    gas_used = Column(Integer, nullable=False)
    miner = Column(String(42), unique=True, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    sha3uncles = Column(String(66), nullable=False)
    extra_data = Column(LargeBinary)
    uncle_count = Column(Integer, nullable=False)
    transaction_count = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'block_number': self.block_number,
            'block_hash': self.block_hash,
            'parent_hash': self.parent_hash,
            'difficulty': self.difficulty,
            'gas_used': self.gas_used,
            'miner': self.miner,
            'timestamp': self.timestamp,
            'sha3uncles': self.sha3uncles,
            'extra_data': self.extra_data,
            'uncle_count': self.uncle_count,
            'transaction_count': self.transaction_count
            }
