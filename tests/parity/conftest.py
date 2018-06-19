import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
    celery_worker_thread,
    drop_session_tables,
    session_block_range_56160_56170,
    session_missing_blocks,
    session_first_block,
)
import logging

logger = logging.getLogger(__name__)
PARITY_SETTINGS = "ParityTestSettings"


@pytest.yield_fixture(scope="module")
def parity_settings():
    parity_settings = session_settings(settings_name=PARITY_SETTINGS)
    yield parity_settings
    drop_session_tables(PARITY_SETTINGS)


@pytest.fixture(scope="module")
def parity_session_block_56160(parity_settings):
    parity_session_block_56160 = session_block_56160(settings_name=
                                                     parity_settings)
    return parity_session_block_56160


@pytest.fixture(scope="module")
def parity_session_block_range_56160_56170(parity_settings):
    parity_session_block_range_56160_56170 = session_block_range_56160_56170(
        settings_name=parity_settings)
    return parity_session_block_range_56160_56170


@pytest.fixture(scope="module")
def parity_session_missing_blocks(parity_settings):
    session_missing_blocks(settings_name=parity_settings)


@pytest.fixture(scope="module")
def parity_session_first_block(parity_settings):
    session_first_block(settings_name=parity_settings)


@pytest.yield_fixture(scope="function")
def parity_start_celery():
    celery_worker = celery_worker_thread(settings_name="TestSettings")
    yield
    celery_worker.stop()
