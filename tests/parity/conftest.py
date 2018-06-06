import pytest
from tests.fixtures.common import (
    session_settings,
    session_block_56160,
)


@pytest.yield_fixture(scope="module")
def parity_settings():
    parity_settings = session_settings(settings_name="TestSettings")
    yield parity_settings


@pytest.yield_fixture(scope="module")
def parity_session_block_56160():
    parity_session_block_56160 = session_block_56160(settings_name=
                                                     "TestSettings")
    yield parity_session_block_56160

    parity_session_block_56160.db_session.close()
