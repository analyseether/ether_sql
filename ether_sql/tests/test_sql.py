from ether_sql.models import base
from ether_sql.scrapper import add_block_number


class TestEmptyDB():

    def test_create_db(self, empty_sql_engine):
        base.metadata.create_all(empty_sql_engine)
        pass

    def test_remove_db(self, empty_sql_engine):
        base.metadata.drop_all(empty_sql_engine)
        pass


class TestEmptyTables():

    def test_push_block(self, empty_table_session):
        session = add_block_number(block_number=0, session=empty_table_session)
        session.commit()
