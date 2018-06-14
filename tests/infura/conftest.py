import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
    celery_worker_thread,
)
import logging

logger = logging.getLogger(__name__)


@pytest.yield_fixture(scope="module")
def infura_settings():
    infura_settings = session_settings(settings_name="TestSettings")
    yield infura_settings


@pytest.yield_fixture(scope="module")
def infura_session_block_56160():
    infura_session_block_56160 = session_block_56160(settings_name=
                                                     "TestSettings")
    yield infura_session_block_56160
    try:
        infura_session_block_56160.db_session.close()
    except AttributeError:
        logger.debug('db_session attribute does not exist')


@pytest.yield_fixture(scope="function")
def infura_start_celery():
    celery_worker = celery_worker_thread(settings_name="TestSettings")
    yield
    celery_worker.stop()
