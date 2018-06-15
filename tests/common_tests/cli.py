import os
from subprocess import call
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.models import (
    base,
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
from tests.common_tests.expected_data import (
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


def export_to_csv_single_thread(node_session_block_56160):
    directory = 'test_export'
    call(["rm", "-rf", directory])
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings',
                                 node_session_block_56160.setting_name,
                                 'sql', 'export_to_csv',
                                 '--directory', directory])
    assert result.exit_code == 0
    # match the names of exported tables
    tables_in_sql = list(base.metadata.tables)
    files_in_directory = os.listdir(directory)
    for sql_table in tables_in_sql:
        assert sql_table+'.csv' in files_in_directory
    call(["rm", "-rf", directory])


def verify_block_contents(node_session_block_56160):
    # comparing values of blocks
    node_session_block_56160.setup_db_session()

    number_of_rows_in_meta_info = node_session_block_56160.db_session.\
        query(MetaInfo).count()
    meta_info_properties_in_sql = node_session_block_56160.db_session.\
        query(MetaInfo).first().to_dict()
    assert number_of_rows_in_meta_info == 1
    print(meta_info_properties_in_sql)
    assert meta_info_properties_in_sql == EXPECTED_META_INFO

    block_properties_in_sql = node_session_block_56160.db_session.\
        query(Blocks).filter_by(block_number=56160).first().to_dict()
    assert block_properties_in_sql == EXPECTED_BLOCK_PROPERTIES

    # comparing values of uncles
    uncle_properties_in_sql = node_session_block_56160.db_session.\
        query(Uncles).filter_by(current_blocknumber=56160).first().to_dict()
    assert uncle_properties_in_sql == EXPECTED_UNCLE_PROPERTIES

    # comparing values of transactions
    transaction_properties_in_sql = node_session_block_56160.db_session.\
        query(Transactions).filter_by(block_number=56160).first().to_dict()
    assert transaction_properties_in_sql == EXPEXTED_TRANSACTION_PROPERTIES

    # comparing values of receipts
    receipt_properties_in_sql = node_session_block_56160.db_session.\
        query(Receipts).filter_by(block_number=56160).first().to_dict()
    assert receipt_properties_in_sql == EXPECTED_RECEIPT_PROPERTIES

    # comparing values of logs
    log_properties_in_sql = node_session_block_56160.db_session.\
        query(Logs).filter_by(block_number=56160).first().to_dict()
    assert log_properties_in_sql == EXPECTED_LOG_PROPERTIES

    # comparing values of traces
    if node_session_block_56160.settings.PARSE_TRACE:
        trace_properties_in_sql = node_session_block_56160.\
            db_session.query(Traces).filter_by(block_number=56160).first().\
            to_dict()
        assert trace_properties_in_sql == EXPECTED_TRACE_PROPERTIES

    # comparing values of states
    if node_session_block_56160.settings.PARSE_STATE_DIFF:
        # comparing values if state diffs
        state_diff_property_in_sql = node_session_block_56160.\
            db_session.query(StateDiff).filter_by(block_number=56160).all()
        for i in range(0, len(state_diff_property_in_sql)):
            assert state_diff_property_in_sql[i].to_dict() == \
                    EXPECTED_STATE_DIFF_PROPERTIES[i]

        # comparing values of storage_diffs
        storage_diff_property_in_sql = node_session_block_56160.\
            db_session.query(StorageDiff).filter_by(block_number=56160).all()
        for i in range(0, len(storage_diff_property_in_sql)):
            assert storage_diff_property_in_sql[i].to_dict() == \
                    EXPECTED_STORAGE_DIFF_PROPERTIES[i]


def push_block_range_single_thread(settings_name):
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings', settings_name,
                                 'scrape_block_range',
                                 '--start_block_number', 0,
                                 '--end_block_number', 10])
    print(result.exc_info)
    assert result.exit_code == 0
