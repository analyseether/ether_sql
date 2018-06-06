from tests.common_tests.sql import (
    drop_upgrade_tables,
    block_number,
)


def test_infura_drop_upgrade_tables(infura_settings):
        drop_upgrade_tables(infura_settings)
        pass


def test_infura_block_number(infura_settings):
        block_number(infura_settings)
        pass
