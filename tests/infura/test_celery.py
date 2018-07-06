from tests.common_tests.celery import (
    push_block_range_multiple_thread,
)


def test_infura_push_block_range_multiple_threads(infura_celery_worker,
                                                  infura_settings):
    push_block_range_multiple_thread()
