from ether_sql.models import base


class TestEmptyDB():

    def test_create_db(self, empty_db_infura_session):
        db_session = empty_db_infura_session.getDbSession()
        base.metadata.create_all(db_session)
        pass

    def test_remove_db(self, empty_db_infura_session):
        db_session = empty_db_infura_session.getDbSession()
        base.metadata.drop_all(db_session)
        pass
