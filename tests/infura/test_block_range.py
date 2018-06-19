from tests.common_tests.block_range import (
    push_block_range_single_thread,
    verify_block_range_single_thread,
)


def test_verify_block_range_single_thread(
        infura_session_block_range_56160_56170):
    verify_block_range_single_thread(
        infura_session_block_range_56160_56170)
    pass


def test_infura_push_block_range(infura_settings):
    push_block_range_single_thread(infura_settings)
    pass
