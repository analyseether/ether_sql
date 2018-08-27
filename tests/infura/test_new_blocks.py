import time
from tests.common_tests.new_blocks import (
    checking_filter_workers,
    put_initial_blocks_in_waiting,
    push_initial_blocks_in_queue,
    verify_pushed_block_56160_contents,
)

class TestInfuraAddingNewBlocks():
    def test_infura_initial_blocks(self, infura_celery_worker):
        put_initial_blocks_in_waiting()

    def test_infura_push_initial_blocks_in_queue(self, infura_celery_worker):
        push_initial_blocks_in_queue()

    def test_verify_pushed_56160_contents(self, infura_celery_worker):
        verify_pushed_block_56160_contents()
