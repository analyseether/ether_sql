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
INFURA_SETTING = "TestSettings"


@pytest.yield_fixture(scope="class")
def infura_settings():
    infura_settings = session_settings(setting_name=INFURA_SETTING)
    yield infura_settings
    drop_session_tables(setting_name=INFURA_SETTING)


@pytest.fixture(scope="class")
def infura_session_block_56160(infura_settings):
    session_block_56160(setting_name=infura_settings)


@pytest.fixture(scope="class")
def infura_session_block_range_56160_56170(infura_settings):
    session_block_range_56160_56170(setting_name=infura_settings)


@pytest.fixture(scope="class")
def infura_session_missing_blocks(infura_settings):
    session_missing_blocks(setting_name=infura_settings)


@pytest.fixture(scope="class")
def infura_session_first_10_blocks(infura_settings):
    session_first_10_blocks(setting_name=infura_settings)


@pytest.yield_fixture(scope="class")
def infura_celery_worker(infura_settings):
    infura_celery_worker = celery_worker(settings_name=infura_settings)
    yield infura_celery_worker
    celery_shutdown(settings_name=infura_settings)
