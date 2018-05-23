from ether_sql.models import base
from sqlalchemy import func
from ether_sql.models import (
    Blocks,
    Transactions,
    Receipts,
    Uncles,
    Logs,
)
from ether_sql.scrapper import add_block_number, scrape_blocks


class TestEmptyDB():
    def test_create_db(self, empty_db_infura_session):
        base.metadata.create_all(empty_db_infura_session.db_engine)

    def test_remove_db(self, empty_db_infura_session):
        base.metadata.drop_all(empty_db_infura_session.db_engine)


class TestEmptyTables():

    def test_verify_block_contents(self,
                                   empty_table_infura_session,
                                   expected_block_properties,
                                   expected_uncle_properties,
                                   expected_transaction_properties,
                                   expected_receipt_properties,
                                   expected_log_properties):

        # first block with a log and an uncle

        empty_table_infura_session = add_block_number(
                                    block_number=56160,
                                    ether_sql_session=empty_table_infura_session)
        empty_table_infura_session.db_session.commit()

        # comparing values of blocks
        block_properties_in_sql = empty_table_infura_session.db_session.query(Blocks).first().to_dict()
        assert block_properties_in_sql == expected_block_properties

        # comparing values of uncles
        uncle_properties_in_sql = empty_table_infura_session.db_session.query(Uncles).first().to_dict()
        assert uncle_properties_in_sql == expected_uncle_properties

        # comparing values of transactions
        transaction_properties_in_sql = empty_table_infura_session.db_session.query(Transactions).first().to_dict()
        assert transaction_properties_in_sql == expected_transaction_properties

        # comparing values of receipts
        receipt_properties_in_sql = empty_table_infura_session.db_session.query(Receipts).first().to_dict()
        assert receipt_properties_in_sql == expected_receipt_properties

        # comparing values of logs
        log_properties_in_sql = empty_table_infura_session.db_session.query(Logs).first().to_dict()
        assert log_properties_in_sql == expected_log_properties

        empty_table_infura_session.db_session.close()
        base.metadata.drop_all(empty_table_infura_session.db_engine)

    def test_push_block_range(self, empty_table_infura_session):

        scrape_blocks(start_block_number=46140,
                      end_block_number=46150,
                      ether_sql_session=empty_table_infura_session)

        # assert the maximum block number
        assert empty_table_infura_session.db_session.query(
                func.max(Blocks.block_number)).scalar() == 46150
        # number of rows in Blocks
        assert empty_table_infura_session.db_session.query(Blocks).count() == 11
        # number of rows in uncles
        assert empty_table_infura_session.db_session.query(Uncles).count() == 1
        # number of rows in transactions
        assert empty_table_infura_session.db_session.query(Transactions).count() == 1
        # number of rows in receipts
        assert empty_table_infura_session.db_session.query(Receipts).count() == 1
        empty_table_infura_session.db_session.close()
        base.metadata.drop_all(empty_table_infura_session.db_engine)
