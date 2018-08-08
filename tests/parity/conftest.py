import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
    drop_session_tables,
    session_block_range_56160_56170,
    session_missing_blocks,
    session_first_10_blocks,
    celery_worker,
    celery_shutdown,
)
import logging

logger = logging.getLogger(__name__)
PARITY_SETTING = "ParityTestSettings"


@pytest.yield_fixture(scope="class")
def parity_settings():
    parity_settings = session_settings(setting_name=PARITY_SETTING)
    yield parity_settings
    drop_session_tables(setting_name=PARITY_SETTING)


@pytest.fixture(scope="class")
def parity_session_block_56160(parity_settings):
    session_block_56160(setting_name=parity_settings)


@pytest.fixture(scope="class")
def parity_session_block_range_56160_56170(parity_settings):
    session_block_range_56160_56170(setting_name=parity_settings)


@pytest.fixture(scope="class")
def parity_session_missing_blocks(parity_settings):
    session_missing_blocks(setting_name=parity_settings)


@pytest.fixture(scope="class")
def parity_session_first_10_blocks(parity_settings):
    session_first_10_blocks(setting_name=parity_settings)


@pytest.yield_fixture(scope="class")
def parity_celery_worker(parity_settings):
    parity_celery_worker = celery_worker(settings_name=parity_settings)
    yield parity_celery_worker
    celery_shutdown(settings_name=parity_settings)
