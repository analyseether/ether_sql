import os
import logging
import json
import pytest
from web3.utils.formatters import hex_to_integer
from eth_utils import to_checksum_address
from ether_sql.models import Blocks
from ether_sql.exceptions import MissingBlocksError
from ether_sql.models.state import State
from ether_sql.globals import get_current_session
from click.testing import CliRunner
from ether_sql.cli import cli

list_initial_missing_blocks = [1, 3]
list_final_missing_blocks = [1, 3, 11, 12, 13, 14, 15]
logger = logging.getLogger(__name__)


def initial_missing_blocks(list_blocks=list_initial_missing_blocks):
    initial_missing_blocks = Blocks.missing_blocks()
    assert len(initial_missing_blocks) == len(list_blocks)
    for index, result in enumerate(initial_missing_blocks):
        assert result.block_number == list_blocks[index]


def final_missing_blocks(list_blocks=list_final_missing_blocks):
    final_missing_blocks = Blocks.missing_blocks(max_block_number=15)
    assert len(final_missing_blocks) == len(list_blocks)
    for index, result in enumerate(final_missing_blocks):
        assert result.block_number == list_blocks[index]


def raise_missing_blocks_error(list_blocks=list_initial_missing_blocks):
    with(pytest.raises(MissingBlocksError,
         message='Cannot construct state at block 10, 2 blocks are missing')):
        State.get_state_at_block()


def fill_missing_blocks(setting_name):
    runner = CliRunner()
    runner.invoke(cli, ['--settings', setting_name,
                        'scrape_block_range',
                        '--end_block_number', 10,
                        '--fill_gaps'])
    assert len(Blocks.missing_blocks(10)) == 0


def match_state_dump_to_state_table(block_number):
    current_session = get_current_session()
    with open('tests/common_tests/balance/balance_{}.json'.format(int(block_number/100))) as data_file:
        data = json.loads(data_file.read())
        state = data['state']
        with current_session.db_session_scope():
            for address in state:
                state_table_row = current_session.db_session.query(State).\
                    filter_by(address=to_checksum_address(address)).first()
                try:
                    assert state_table_row.balance == hex_to_integer(state[address]['balance'])
                    assert state_table_row.nonce == hex_to_integer(state[address]['nonce'])
                    if 'code' in state[address].keys():
                        assert state_table_row.code == "0x"+state[address]['code']
                        if state_table_row.storage is not None:
                            for storage in state_table_row.storage:
                                try:
                                    storage.storage = state[address]['storage'][storage.position]
                                except:
                                    logger.debug('{}, pos: {}, code: {}'.format(address, storage.position, state_table_row.code))
                except (AttributeError, AssertionError) as a:
                    if state_table_row is None:
                        logger.debug('(table, csv); address:{}, balance (_, {})'\
                                     .format(address, hex_to_integer(state[address]['balance'])))
                    else:
                        logger.debug('(table, csv); address: {}, balance: ({}, {})'\
                                     .format(address, state_table_row.balance,
                                             hex_to_integer(state[address]['balance'])))
                    raise a
                except KeyError as k:
                    logger.debug('(table, csv); address {}, code: ({},_) '\
                                     .format(address, state_table_row.code))
                    raise k


def check_state_at_block_0():
    State.get_state_at_block(0)
    match_state_dump_to_state_table(0)


def check_state_at_block_100():
    State.get_state_at_block(100)
    match_state_dump_to_state_table(100)
# TODO write a test which extracts the current state after filling missing blocks
