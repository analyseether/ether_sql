import time
from tests.common_tests.new_blocks import (
    checking_filter_workers,
    put_initial_blocks_in_waiting,
    push_initial_blocks_in_queue,
    verify_pushed_block_56160_contents,
)

class TestParityCheckingFilterWorker():
    def test_parity_checking_filter_workers(self, parity_celery_filter_worker):
        checking_filter_workers(parity_celery_filter_worker)

class TestParityAddingNewBlocks():
    def test_parity_initial_blocks(self, parity_celery_worker):
        put_initial_blocks_in_waiting()

    def test_parity_push_initial_blocks_in_queue(self, parity_celery_worker):
        push_initial_blocks_in_queue()

    def test_verify_pushed_56160_contents(self, parity_celery_worker):
        verify_pushed_block_56160_contents()
