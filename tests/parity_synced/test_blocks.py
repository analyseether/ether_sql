import pytest
from tests.common_tests.blocks import (
    initial_missing_blocks,
    final_missing_blocks,
    raise_missing_blocks_error,
    fill_missing_blocks,
    verify_block_range_56160_56170,
    verify_state_at_block,
    verify_block_56160_contents
)


class TestParityMissingBlocks():
    def test_parity_initial_missing_blocks(self, parity_session_missing_blocks):
        initial_missing_blocks()

    def test_parity_final_missing_blocks(self, parity_session_missing_blocks):
        final_missing_blocks()

    def test_parity_raise_missing_blocks_error(self, parity_session_missing_blocks):
        raise_missing_blocks_error()

    def test_parity_fill_missing_blocks(self, parity_session_missing_blocks):
        fill_missing_blocks()


@pytest.mark.medium
class TestParityFirst10Blocks():
    def test_parity_verify_state_at_block_0(self, parity_session_first_10_blocks):
        verify_state_at_block(0)

    def test_parity_verify_state_at_block_10(self, parity_session_first_10_blocks):
        verify_state_at_block(10)


class TestParityBlocks_56160_56170():
    def test_verify_block_range_56160_56170(
            self, parity_session_block_range_56160_56170):
        verify_block_range_56160_56170()

    def test_parity_verify_block_56160_contents(
            self, parity_session_block_range_56160_56170):
        verify_block_56160_contents()
        pass
