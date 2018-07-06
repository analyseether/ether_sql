import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
    drop_session_tables,
    session_block_range_56160_56170,
    celery_worker,
    celery_shutdown,
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


@pytest.yield_fixture(scope="module")
def parity_celery_worker(parity_settings):
    parity_celery_worker = celery_worker(settings_name=parity_settings)
    yield parity_celery_worker
    celery_shutdown(settings_name=parity_settings)
