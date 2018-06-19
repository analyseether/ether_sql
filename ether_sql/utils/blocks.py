from sqlalchemy import func
from ether_sql.globals import get_current_session
from ether_sql.models import Blocks


def get_max_block_number():
    current_session = get_current_session()
    with current_session.db_session_scope():
        max_block_number = current_session.db_session.query(
                                func.max(Blocks.block_number)).scalar()
    return max_block_number
