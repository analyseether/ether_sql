from tests.common_tests.ether import (
    listening_to_node,
    ether_block_number
)


def test_infura_listening_to_node(infura_settings):
    listening_to_node(infura_settings)
    pass


def test_infura_ether_block_number(infura_settings):
    ether_block_number(infura_settings)
    pass
