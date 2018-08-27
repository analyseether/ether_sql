from tests.common_tests.celery import (
    push_block_range_multiple_thread,
)


def test_infura_push_block_range_multiple_threads(parity_celery_worker,
                                                  parity_settings):
    push_block_range_multiple_thread()
