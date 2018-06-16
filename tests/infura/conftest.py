import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
    celery_worker_thread,
    drop_session_tables,
    session_block_range_56160_56170,
)
import logging

logger = logging.getLogger(__name__)
INFURA_SETTING = "TestSettings"


@pytest.yield_fixture(scope="module")
def infura_settings():
    infura_settings = session_settings(settings_name=INFURA_SETTING)
    yield infura_settings
    drop_session_tables(settings_name=INFURA_SETTING)


@pytest.yield_fixture(scope="module")
def infura_session_block_56160(infura_settings):
    infura_session_block_56160 = session_block_56160(settings_name=
                                                     infura_settings)
    yield infura_session_block_56160
    try:
        infura_session_block_56160.db_session.close()
    except AttributeError:
        logger.debug('db_session attribute does not exist')


@pytest.yield_fixture(scope="module")
def infura_session_block_range_56160_56170(infura_settings):
    infura_session_block_range_56160_56170 = session_block_range_56160_56170(
        settings_name=infura_settings)
    infura_session_block_range_56160_56170.setup_db_session()
    yield infura_session_block_range_56160_56170
    try:
        infura_session_block_range_56160_56170.db_session.close()
    except AttributeError:
        logger.debug('db_session attribute does not exist')


@pytest.yield_fixture(scope="module")
def infura_start_celery():
    celery_worker = celery_worker_thread(settings_name=INFURA_SETTING)
    yield
    celery_worker.stop()
