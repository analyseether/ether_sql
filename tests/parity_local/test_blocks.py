from ether_sql.globals import get_current_session
from click.testing import CliRunner
from ether_sql.cli import cli
import logging

logger = logging.getLogger(__name__)

def test_block_number(parity_local_settings):
    current_session = get_current_session()
    print(current_session.w3.eth.blockNumber)
    runner = CliRunner()
    runner.invoke(cli, ['--settings', parity_local_settings,
                        'scrape_block_range',
                        '--start_block_number', 1])
    result = runner.invoke(cli, ['--settings', parity_local_settings,
                           'sql', 'blocknumber'])
    print('{}'.format(result))
    assert 1 == 2
