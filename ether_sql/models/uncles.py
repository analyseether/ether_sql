from sqlalchemy import Column, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy import Text
from ethereum import utils

from ether_sql.models import base


class Uncles(base):

    """
    Class defining an uncle in the ethereum blockchain, its properties are more
    accurately defined in the ethereum yellow paper https://github.com/ethereum/yellowpaper.

    :param str uncle_hash: The Keccak 256-bit hash of this uncle
    :param int uncle_blocknumber: Number of blocks behind this uncle
    :param str parent_hash: The Keccak 256-bit hash of the parent of this uncle
    :param int difficulty: Difficulty level of this block
    :param int current_blocknumber: Block number where this uncle was included
    :param int gas_used: Total gas used by the transactions in this uncle
    :param str miner: Address of account where all corresponding uncle rewards are transferred
    :param int timestamp: Unix time at the at this uncles inception
    :param str sha3uncles: Keccak 256-bit hash of the uncles portion of this uncle
    :param bytes extra_data: Byte array of 32 bytes or less containing extra data of this block
    :param int gas_limit: Current maximum gas expenditure per block

    """
    __tablename__ = 'uncles'

    uncle_hash = Column(String(66), primary_key=True, unique=True, index=True)
    uncle_blocknumber = Column(Numeric, nullable=False)
    parent_hash = Column(String(66), nullable=False)
    difficulty = Column(String(66), unique=True, nullable=False)
    current_blocknumber = Column(Numeric,  ForeignKey('blocks.block_number'),
                                 unique=True)
    gas_used = Column(Numeric, nullable=False)
    miner = Column(String(42), nullable=False)
    timestamp = Column(TIMESTAMP)
    sha3uncles = Column(String(66), nullable=False)
    extra_data = Column(Text)
    gas_limit = Column(Numeric, nullable=False)

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

    @classmethod
    def add_uncle(cls, uncle_data, block_number, iso_timestamp):
        """
        Creates a new block object from data received from JSON-RPC call
        eth_getUncleByBlockNumberAndIndex.

        :param dict uncle_data: uncle data received from JSON RPC call
        :param int block_number: block number where this uncle was included
        :param datetime iso_timestamp: timestamp when the block was mined

        :return Uncle: return completed uncle
        """

        uncle = cls(uncle_hash=uncle_data['hash'],
                    uncle_blocknumber=utils.parse_int_or_hex(uncle_data['number']),  # 'uncle_blocknumber'
                    parent_hash=uncle_data['parentHash'],  # parent_hash
                    difficulty=utils.parse_int_or_hex(uncle_data['difficulty']),  # 'difficulty
                    current_blocknumber=block_number,  # current_blocknumber
                    gas_used=utils.parse_int_or_hex(uncle_data['gasUsed']),  # gas_used
                    miner=uncle_data['miner'],  # miner
                    timestamp=iso_timestamp,
                    sha3uncles=uncle_data['sha3Uncles'],  # SHA3uncles
                    extra_data=uncle_data['extraData'],  # extra_data
                    gas_limit=utils.parse_int_or_hex(uncle_data['gasLimit']))

        return uncle
