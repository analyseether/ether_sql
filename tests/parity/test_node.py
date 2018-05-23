def test_listening_to_parity_node(empty_db_parity_session):
    listening = empty_db_parity_session.w3.isConnected()
    assert listening is True
