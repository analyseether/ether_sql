from click.testing import CliRunner
from sqlalchemy import func
from ether_sql.cli import cli
from ether_sql.models import (
    Blocks,
    Transactions,
    Receipts,
    Uncles,
    Logs,
    Traces,
)


class TestEmptyTables():

    def test_verify_block_contents(self,
                                   parity_settings,
                                   parity_session,
                                   expected_block_properties,
                                   expected_uncle_properties,
                                   expected_transaction_properties,
                                   expected_receipt_properties,
                                   expected_log_properties,
                                   expected_trace_properties,):

        # first block with a log and an uncle
        runner = CliRunner()
        result = runner.invoke(cli, ['--settings', parity_settings,
                                     'scrape_block', '--block_number', 56160])
        assert result.exit_code == 0

        # comparing values of blocks
        block_properties_in_sql = parity_session.db_session.query(Blocks).first().to_dict()
        assert block_properties_in_sql == expected_block_properties

        # comparing values of uncles
        uncle_properties_in_sql = parity_session.db_session.query(Uncles).first().to_dict()
        assert uncle_properties_in_sql == expected_uncle_properties

        # comparing values of transactions
        transaction_properties_in_sql = parity_session.db_session.query(Transactions).first().to_dict()
        assert transaction_properties_in_sql == expected_transaction_properties

        # comparing values of receipts
        receipt_properties_in_sql = parity_session.db_session.query(Receipts).first().to_dict()
        assert receipt_properties_in_sql == expected_receipt_properties

        # comparing values of logs
        log_properties_in_sql = parity_session.db_session.query(Logs).first().to_dict()
        assert log_properties_in_sql == expected_log_properties

        # comparing values of traces
        trace_properties_in_sql = parity_session.db_session.query(Traces).first().to_dict()
        assert trace_properties_in_sql == expected_trace_properties

        parity_session.db_session.close()

    def test_push_block_range(self,
                              parity_settings,
                              parity_session,):

        runner = CliRunner()
        result = runner.invoke(cli, ['--settings', parity_settings,
                                     'scrape_block_range',
                                     '--start_block_number', 46140,
                                     '--end_block_number', 46150])
        assert result.exit_code == 0

        # assert the maximum block number
        assert parity_session.db_session.query(
                func.max(Blocks.block_number)).scalar() == 46150
        # number of rows in Blocks
        assert parity_session.db_session.query(Blocks).count() == 11
        # number of rows in uncles
        assert parity_session.db_session.query(Uncles).count() == 1
        # number of rows in transactions
        assert parity_session.db_session.query(Transactions).count() == 1
        # number of rows in receipts
        assert parity_session.db_session.query(Receipts).count() == 1
        parity_session.db_session.close()
