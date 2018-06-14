from tests.common_tests.celery import (
    push_block_range_multiple_threads,
)


def test_infura_push_block_range_multiple_threads(infura_start_celery,
                                                  infura_settings):
    push_block_range_multiple_threads(infura_settings)
    pass
