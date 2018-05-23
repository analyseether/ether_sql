def test_listening_to_infura_node(empty_db_infura_session):
    listening = empty_db_infura_session.w3.isConnected()
    assert listening is True
