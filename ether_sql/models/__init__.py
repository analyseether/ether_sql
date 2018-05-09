from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()

# Initializing these classes here to remove sqlalchemy.exc.InvalidRequestError
# More here: https://stackoverflow.com/a/45613994/3420738
from ether_sql.models.blocks import Blocks
from ether_sql.models.transactions import Transactions
from ether_sql.models.uncles import Uncles
from ether_sql.models.receipts import Receipts
from ether_sql.models.logs import Logs
from ether_sql.models.traces import Traces
