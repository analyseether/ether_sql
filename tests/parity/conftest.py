import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
    celery_worker_thread,
)
import logging

logger = logging.getLogger(__name__)


@pytest.yield_fixture(scope="module")
def parity_settings():
    parity_settings = session_settings(settings_name="ParityTestSettings")
    yield parity_settings


@pytest.yield_fixture(scope="module")
def parity_session_block_56160():
    parity_session_block_56160 = session_block_56160(settings_name=
                                                     "ParityTestSettings")
    yield parity_session_block_56160

    try:
        parity_session_block_56160.db_session.close()
    except AttributeError:
        logger.debug('db_session attribute does not exist')


@pytest.yield_fixture(scope="function")
def parity_start_celery():
    celery_worker = celery_worker_thread(settings_name="TestSettings")
    yield
    celery_worker.stop()
