from tests.common_tests.blocks import (
    initial_missing_blocks,
    final_missing_blocks,
    raise_missing_blocks_error,
    fill_missing_blocks,
    check_state_at_block_0,
    check_state_at_block_100,
)
from ether_sql.globals import get_current_session


def test_infura_initial_missing_blocks(infura_session_missing_blocks):
    initial_missing_blocks()


def test_infura_final_missing_blocks(infura_session_missing_blocks):
    final_missing_blocks()


def test_infura_raise_missing_blocks_error(infura_session_missing_blocks):
    raise_missing_blocks_error()


def test_infura_fill_missing_blocks(infura_session_missing_blocks):
    setting_name = get_current_session().setting_name
    fill_missing_blocks(setting_name)


def test_infura_check_state_at_block_0(infura_session_first_block):
    check_state_at_block_0()
