import pytest


def test_listening_to_infura_node(empty_db_infura_session):
    listening = empty_db_infura_session.w3.isConnected()
    assert listening is True


def test_listening_to_parity_node(empty_db_parity_session):
    pytest.xfail('not connected to a parity node')
    listening = empty_db_parity_session.w3.isConnected()
    assert listening is True
