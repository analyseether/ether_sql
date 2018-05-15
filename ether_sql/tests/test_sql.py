from ether_sql.models import base
from ether_sql.models import Blocks, Transactions, Receipts, Uncles
from ether_sql.scrapper import add_block_number, scrape_blocks
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker


class TestEmptyDB():

    def test_create_db(self, empty_sql_engine):
        base.metadata.create_all(empty_sql_engine)
        pass

    def test_remove_db(self, empty_sql_engine):
        base.metadata.drop_all(empty_sql_engine)
        pass


class TestEmptyTables():

    def test_push_block_0(self, empty_table_engine):

        DBSession = sessionmaker(bind=empty_table_engine)
        empty_table_session = DBSession()

        test_db_session = add_block_number(block_number=0, session=empty_table_session)
        test_db_session.commit()

        # assert the maximum block number
        assert test_db_session.query(
                func.max(Blocks.block_number)).scalar() == 0
        # number of rows in Blocks
        assert test_db_session.query(Blocks).count() == 1
        # number of rows in uncles
        assert test_db_session.query(Uncles).count() == 0
        # number of rows in transactions
        assert test_db_session.query(Transactions).count() == 0
        # number of rows in receipts
        assert test_db_session.query(Receipts).count() == 0
        test_db_session.close()

        base.metadata.drop_all(empty_table_engine)

    def test_push_block_range(self, empty_table_engine):
        DBSession = sessionmaker(bind=empty_table_engine)
        empty_table_session = DBSession()

        scrape_blocks(sql_block_number=46140, node_block_number=46150,
                      session=empty_table_session)
        # assert the maximum block number
        assert empty_table_session.query(
                func.max(Blocks.block_number)).scalar() == 46150
        # number of rows in Blocks
        assert empty_table_session.query(Blocks).count() == 10
        # number of rows in uncles
        assert empty_table_session.query(Uncles).count() == 1
        # number of rows in transactions
        assert empty_table_session.query(Transactions).count() == 1
        # number of rows in receipts
        assert empty_table_session.query(Receipts).count() == 1
        empty_table_session.close()
        base.metadata.drop_all(empty_table_engine)
