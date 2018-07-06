from click.testing import CliRunner
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
from ether_sql.cli import cli


def push_block_range_single_thread(settings_name):
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings', settings_name,
                                 'scrape_block_range',
                                 '--start_block_number', 0,
                                 '--end_block_number', 10])
    print(result.exc_info)
    assert result.exit_code == 0


def verify_block_range(session):
    with session.db_session_scope():

        assert session.db_session.query(Blocks).count() == 11
        assert session.db_session.query(Transactions).count() == 3
        assert session.db_session.query(Receipts).count() == 3
        assert session.db_session.query(Logs).count() == 1
        assert session.db_session.query(Uncles).count() == 1
        # assert session.db_session.query(MetaInfo).count() == 1

        if session.settings.PARSE_TRACE:
            assert session.db_session.query(Traces).count() == 3

        if session.settings.PARSE_STATE_DIFF:
            assert session.db_session.query(StateDiff).count() == 20
            assert session.db_session.query(StorageDiff).count() == 2
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='miner').count() == 11
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='fees').count() == 3
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='sender').count() == 3
            assert session.db_session.query(StateDiff).filter_by(
                state_diff_type='uncle').count() == 1
