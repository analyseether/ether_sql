from tests.common_tests.sql import (
    drop_upgrade_tables,
    block_number,
)


def test_parity_drop_upgrade_tables(parity_settings):
        drop_upgrade_tables(parity_settings)
        pass


def test_parity_block_number(parity_settings):
        block_number(parity_settings)
        pass
