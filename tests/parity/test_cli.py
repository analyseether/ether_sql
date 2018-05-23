from sqlalchemy import func
from click.testing import CliRunner
from ether_sql.models import (
    Blocks,
    Transactions,
    Receipts,
    Uncles,
    Logs,
)
from ether_sql.cli import cli


class TestEmptyTables():

    def test_verify_block_contents(self,
                                   empty_table_engine,
                                   expected_block_properties,
                                   expected_uncle_properties,
                                   expected_transaction_properties,
                                   expected_receipt_properties,
                                   expected_log_values):

        # first block with a log and an uncle

        test_db_session = add_block_number(block_number=56160,
                                           session=empty_table_session)
        test_db_session.commit()

        # comparing values of blocks
        block_properties_in_sql = test_db_session.query(Blocks).first().to_dict()
        assert block_properties_in_sql == expected_block_properties

        # comparing values of uncles
        uncle_properties_in_sql = test_db_session.query(Uncles).first().to_dict()
        assert uncle_properties_in_sql == expected_uncle_properties

        # comparing values of transactions
        transaction_properties_in_sql = test_db_session.query(Transactions).first().to_dict()
        assert transaction_properties_in_sql == expected_transaction_properties

        # comparing values of receipts
        receipt_properties_in_sql = test_db_session.query(Receipts).first().to_dict()
        assert receipt_properties_in_sql == expected_receipt_properties

        # comparing values of logs
        log_properties_in_sql = test_db_session.query(Logs).first().to_dict()
        assert log_properties_in_sql == expected_log_values

        empty_table_session.close()
        base.metadata.drop_all(empty_table_engine)

    def test_push_block_range(self, empty_table_engine):
        DBSession = sessionmaker(bind=empty_table_engine)
        empty_table_session = DBSession()

        scrape_blocks(start_block_number=46140, end_block_number=46150,
                      session=empty_table_session)
        # assert the maximum block number
        assert empty_table_session.query(
                func.max(Blocks.block_number)).scalar() == 46150
        # number of rows in Blocks
        assert empty_table_session.query(Blocks).count() == 11
        # number of rows in uncles
        assert empty_table_session.query(Uncles).count() == 1
        # number of rows in transactions
        assert empty_table_session.query(Transactions).count() == 1
        # number of rows in receipts
        assert empty_table_session.query(Receipts).count() == 1
        empty_table_session.close()
        base.metadata.drop_all(empty_table_engine)
