from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

base = declarative_base(metadata=metadata)

# Initializing these classes here to remove sqlalchemy.exc.InvalidRequestError
# More here: https://stackoverflow.com/a/45613994/3420738
from ether_sql.models.blocks import Blocks
from ether_sql.models.transactions import Transactions
from ether_sql.models.uncles import Uncles
from ether_sql.models.receipts import Receipts
from ether_sql.models.logs import Logs
from ether_sql.models.traces import Traces
from ether_sql.models.meta_info import MetaInfo
from ether_sql.models.state_diff import StateDiff
from ether_sql.models.storage_diff import StorageDiff
from ether_sql.models.state import State
from ether_sql.models.storage import Storage
from ether_sql.models.block_task_meta import BlockTaskMeta
