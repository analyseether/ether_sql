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
INFURA_SETTING = "TestSettings"


@pytest.yield_fixture(scope="module")
def infura_settings():
    infura_settings = session_settings(settings_name=INFURA_SETTING)
    yield infura_settings
    drop_session_tables(settings_name=INFURA_SETTING)


@pytest.fixture(scope="module")
def infura_session_block_56160(infura_settings):
    infura_session_block_56160 = session_block_56160(settings_name=
                                                     infura_settings)
    return infura_session_block_56160


@pytest.fixture(scope="module")
def infura_session_block_range_56160_56170(infura_settings):
    infura_session_block_range_56160_56170 = session_block_range_56160_56170(
        settings_name=infura_settings)
    return infura_session_block_range_56160_56170


@pytest.yield_fixture(scope="module")
def infura_celery_worker(infura_settings):
    infura_celery_worker = celery_worker(settings_name=infura_settings)
    yield infura_celery_worker
    celery_shutdown(settings_name=infura_settings)
