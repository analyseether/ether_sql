from ether_sql import node_session


def test_listening_to_node():
    listening = node_session.net_listening()
    assert listening is True
