import json
from ether_sql.globals import get_current_session
from click.testing import CliRunner
from ether_sql.cli import cli
from eth_utils import to_checksum_address
from web3.utils.formatters import hex_to_integer
from ether_sql.models import State
import logging

logger = logging.getLogger(__name__)

def add_block(setting_name, block_number):
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings', setting_name,
                        'scrape_block', '--block_number', block_number])
    logger.debug(result.output)

def match_state_dump_to_state_table(block_number):
    current_session = get_current_session()
    with open('tests/fixtures/balance/balance_{}.json'.format(block_number)) as data_file:
        data = json.loads(data_file.read())
        state = data['state']
    with current_session.db_session_scope():
        for address in state:
            state_table_row = current_session.db_session.query(State).\
                filter_by(address=to_checksum_address(address)).first()
            assert state_table_row.balance == hex_to_integer(state[address]['balance'])
            assert state_table_row.nonce == hex_to_integer(state[address]['nonce'])
            if 'code' in state[address].keys():
                assert state_table_row.code == "0x"+state[address]['code']
                if state_table_row.storage is not None:
                    for storage in state_table_row.storage:
                        storage.storage = state[address]['storage'][storage.position]
