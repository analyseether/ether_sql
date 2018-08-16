from ether_sql.globals import get_current_session
from click.testing import CliRunner
from ether_sql.cli import cli
import logging
from ether_sql.models import (
    Blocks,
    Transactions,
    Receipts,
    Uncles,
    Logs,
    Traces,
    MetaInfo,
    StateDiff,
    StorageDiff,
)

logger = logging.getLogger(__name__)

def test_count_sql_contents(parity_push_blocks_in_sql):
    session = get_current_session()
    with session.db_session_scope():
        assert session.db_session.query(Blocks).count() == 6
        assert session.db_session.query(Transactions).count() == 4
        assert session.db_session.query(Receipts).count() == 4
        assert session.db_session.query(Uncles).count() == 0

        if session.settings.PARSE_TRACE:
            assert session.db_session.query(Traces).count() == 4

        if session.settings.PARSE_STATE_DIFF:
            assert session.db_session.query(StateDiff).count() == 12
            assert session.db_session.query(StorageDiff).count() == 0
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='miner').count() == 6
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='fees').count() == 0
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='sender').count() == 4
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='uncle').count() == 0
