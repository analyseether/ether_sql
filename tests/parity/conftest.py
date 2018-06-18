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
PARITY_SETTINGS = "ParityTestSettings"


@pytest.yield_fixture(scope="module")
def parity_settings():
    parity_settings = session_settings(settings_name=PARITY_SETTINGS)
    yield parity_settings
    drop_session_tables(PARITY_SETTINGS)


@pytest.yield_fixture(scope="module")
def parity_session_block_56160(parity_settings):
    parity_session_block_56160 = session_block_56160(settings_name=
                                                     parity_settings)
    yield parity_session_block_56160
    try:
        parity_session_block_56160.db_session.close()
    except AttributeError:
        logger.debug('db_session attribute does not exist')


@pytest.yield_fixture(scope="module")
def parity_session_block_range_56160_56170(parity_settings):
    parity_session_block_range_56160_56170 = session_block_range_56160_56170(
        settings_name=parity_settings)
    parity_session_block_range_56160_56170.setup_db_session()
    yield parity_session_block_range_56160_56170
    try:
        parity_session_block_range_56160_56170.db_session.close()
    except AttributeError:
        logger.debug('db_session attribute does not exist')


@pytest.yield_fixture(scope="function")
def parity_start_celery():
    celery_worker = celery_worker_thread(settings_name="TestSettings")
    yield
    celery_worker.stop()
