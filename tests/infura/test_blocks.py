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


class TestInfuraMissingBlocks():
    def test_infura_initial_missing_blocks(self, infura_session_missing_blocks):
        initial_missing_blocks()

    def test_infura_final_missing_blocks(self, infura_session_missing_blocks):
        final_missing_blocks()

    def test_infura_raise_missing_blocks_error(self, infura_session_missing_blocks):
        raise_missing_blocks_error()

    def test_infura_fill_missing_blocks(self, infura_session_missing_blocks):
        fill_missing_blocks()


@pytest.mark.medium
class TestInfuraFirst10Blocks():
    def test_infura_verify_state_at_block_0(self, infura_session_first_10_blocks):
        verify_state_at_block(0)

    def test_infura_verify_state_at_block_10(self, infura_session_first_10_blocks):
        verify_state_at_block(10)


class TestInfuraBlocks_56160_56170():
    def test_verify_block_range_56160_56170(
            self, infura_session_block_range_56160_56170):
        verify_block_range_56160_56170()

    def test_infura_verify_block_56160_contents(
            self, infura_session_block_range_56160_56170):
        verify_block_56160_contents()
        pass
