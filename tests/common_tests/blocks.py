import logging
import json
import pytest
from ether_sql.exceptions import MissingBlocksError
from ether_sql.models.state import State
from ether_sql.globals import get_current_session
from click.testing import CliRunner
from ether_sql.cli import cli
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
from ether_sql.tasks.scrapper import remove_block_number
from tests.common_tests.utils import match_state_dump_to_state_table
from tests.fixtures.expected_data import (
    EXPECTED_BLOCK_PROPERTIES,
    EXPECTED_UNCLE_PROPERTIES,
    EXPEXTED_TRANSACTION_PROPERTIES,
    EXPECTED_RECEIPT_PROPERTIES,
    EXPECTED_LOG_PROPERTIES,
    EXPECTED_TRACE_PROPERTIES,
    EXPECTED_META_INFO,
    EXPECTED_STATE_DIFF_PROPERTIES,
    EXPECTED_STORAGE_DIFF_PROPERTIES,
)

list_initial_missing_blocks = [1, 3]
list_final_missing_blocks = [1, 3, 11, 12, 13, 14, 15]
logger = logging.getLogger(__name__)


def initial_missing_blocks(list_blocks=list_initial_missing_blocks):
    initial_missing_blocks = Blocks.missing_blocks()
    assert len(initial_missing_blocks) == len(list_blocks)
    for index, result in enumerate(initial_missing_blocks):
        assert result.block_number == list_blocks[index]


def final_missing_blocks(list_blocks=list_final_missing_blocks):
    final_missing_blocks = Blocks.missing_blocks(max_block_number=15)
    assert len(final_missing_blocks) == len(list_blocks)
    for index, result in enumerate(final_missing_blocks):
        assert result.block_number == list_blocks[index]


def raise_missing_blocks_error(list_blocks=list_initial_missing_blocks):
    with(pytest.raises(MissingBlocksError,
         message='Cannot construct state at block 10, 2 blocks are missing')):
        State.get_state_at_block()


def fill_missing_blocks():
    session = get_current_session()
    runner = CliRunner()
    runner.invoke(cli, ['--settings', session.setting_name,
                        'scrape_block_range',
                        '--end_block_number', 10,
                        '--fill_gaps'])
    assert len(Blocks.missing_blocks(10)) == 0


def verify_state_at_block(block_number):
    State.get_state_at_block(block_number)
    match_state_dump_to_state_table(block_number)


def verify_block_range_56160_56170():
    session = get_current_session()
    with session.db_session_scope():
        logger.debug('Total blocks {}'.format(session.db_session.query(Blocks).count()))
        assert session.db_session.query(Blocks).count() == 11
        assert session.db_session.query(Transactions).count() == 3
        assert session.db_session.query(Receipts).count() == 3
        assert session.db_session.query(Logs).count() == 1
        assert session.db_session.query(Uncles).count() == 1
        # assert session.db_session.query(MetaInfo).count() == 1

        number_of_rows_in_meta_info = session.db_session.\
            query(MetaInfo).count()
        meta_info_properties_in_sql = session.db_session.\
            query(MetaInfo).first().to_dict()
        assert number_of_rows_in_meta_info == 1
        print(meta_info_properties_in_sql)
        assert meta_info_properties_in_sql == EXPECTED_META_INFO

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


def verify_block_56160_contents():
    # comparing values of blocks
    session = get_current_session()
    with session.db_session_scope():

        block_properties_in_sql = session.db_session.\
            query(Blocks).filter_by(block_number=56160).first().to_dict()
        assert block_properties_in_sql == EXPECTED_BLOCK_PROPERTIES

        # comparing values of uncles
        uncle_properties_in_sql = session.db_session.\
            query(Uncles).filter_by(current_blocknumber=56160).first().to_dict()
        assert uncle_properties_in_sql == EXPECTED_UNCLE_PROPERTIES

        # comparing values of transactions
        transaction_properties_in_sql = session.db_session.\
            query(Transactions).filter_by(block_number=56160).first().to_dict()
        assert transaction_properties_in_sql == EXPEXTED_TRANSACTION_PROPERTIES

        # comparing values of receipts
        receipt_properties_in_sql = session.db_session.\
            query(Receipts).filter_by(block_number=56160).first().to_dict()
        assert receipt_properties_in_sql == EXPECTED_RECEIPT_PROPERTIES

        # comparing values of logs
        log_properties_in_sql = session.db_session.\
            query(Logs).filter_by(block_number=56160).first().to_dict()
        assert log_properties_in_sql == EXPECTED_LOG_PROPERTIES

        # comparing values of traces
        if session.settings.PARSE_TRACE:
            trace_properties_in_sql = session.\
                db_session.query(Traces).filter_by(block_number=56160).first().\
                to_dict()
            assert trace_properties_in_sql == EXPECTED_TRACE_PROPERTIES

        # comparing values of states
        if session.settings.PARSE_STATE_DIFF:
            # comparing values if state diffs
            state_diff_property_in_sql = session.\
                db_session.query(StateDiff).filter_by(block_number=56160).all()
            for i in range(0, len(state_diff_property_in_sql)):
                assert state_diff_property_in_sql[i].to_dict() == \
                    EXPECTED_STATE_DIFF_PROPERTIES[i]

        # comparing values of storage_diffs
            storage_diff_property_in_sql = session.\
                db_session.query(StorageDiff).filter_by(block_number=56160).all()
            for i in range(0, len(storage_diff_property_in_sql)):
                assert storage_diff_property_in_sql[i].to_dict() == \
                    EXPECTED_STORAGE_DIFF_PROPERTIES[i]


def verify_removed_block_range_56160_56170():
    for i in range(56160, 56171):
        remove_block_number(i)
    session = get_current_session()
    with session.db_session_scope():
        assert session.db_session.query(Blocks).count() == 0
        assert session.db_session.query(Transactions).count() == 0
        assert session.db_session.query(Receipts).count() == 0
        assert session.db_session.query(Logs).count() == 0
        assert session.db_session.query(Uncles).count() == 0
        assert session.db_session.query(Traces).count() == 0
        assert session.db_session.query(StateDiff).count() == 0
        assert session.db_session.query(StorageDiff).count() == 0
