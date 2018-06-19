import os
import logging
import json
import pytest
from web3.utils.formatters import hex_to_integer
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
    logger.debug(os.getcwd())
    with open('tests/common_tests/balance/balance_{}.json'.format(int(block_number/10))) as data_file:
        data = json.loads(data_file.read())
        state = data['state']
        with current_session.db_session_scope():
            for address in state:
                state_table_row = current_session.db_session.query(State).\
                    filter_by(address=address).first()
                try:
                    assert state_table_row.balance == hex_to_integer(state[address]['balance'])
                except AttributeError:
                    logger.debug(address)
                # assert state_table_row.nonce == hex_to_integer(state[address]['nonce'])


def check_state_at_block_0():
    State.get_state_at_block(0)
    match_state_dump_to_state_table(0)


def check_state_at_block_100():
    State.get_state_at_block(100)
    match_state_dump_to_state_table(100)
# TODO write a test which extracts the current state after filling missing blocks
