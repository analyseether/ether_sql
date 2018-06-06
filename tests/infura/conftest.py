import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
)


@pytest.yield_fixture(scope="module")
def infura_settings():
    infura_settings = session_settings(settings_name="TestSettings")
    yield infura_settings


@pytest.yield_fixture(scope="module")
def infura_session_block_56160():
    infura_session_block_56160 = session_block_56160(settings_name=
                                                     "TestSettings")
    yield infura_session_block_56160

    infura_session_block_56160.db_session.close()
