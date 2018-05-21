from ether_sql import w3


def test_listening_to_node():
    listening = w3.isConnected()
    assert listening is True
