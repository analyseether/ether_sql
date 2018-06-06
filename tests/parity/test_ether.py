from tests.common_tests.ether import (
    listening_to_node,
    ether_block_number
)


def test_parity_listening_to_node(parity_settings):
    listening_to_node(parity_settings)
    pass


def test_parity_ether_block_number(parity_settings):
    ether_block_number(parity_settings)
    pass
