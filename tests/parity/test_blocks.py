from tests.common_tests.blocks import (
    initial_missing_blocks,
    final_missing_blocks,
    raise_missing_blocks_error,
    fill_missing_blocks,
    check_state_at_block_0,
    check_state_at_block_100,
)
from ether_sql.globals import get_current_session


def test_parity_initial_missing_blocks(parity_session_missing_blocks):
    initial_missing_blocks()


def test_parity_final_missing_blocks(parity_session_missing_blocks):
    final_missing_blocks()


def test_parity_raise_missing_blocks_error(parity_session_missing_blocks):
    raise_missing_blocks_error()


def test_parity_fill_missing_blocks(parity_session_missing_blocks):
    setting_name = get_current_session().setting_name
    fill_missing_blocks(setting_name)


def test_parity_check_state_at_block_0(parity_session_first_block):
    check_state_at_block_0()
