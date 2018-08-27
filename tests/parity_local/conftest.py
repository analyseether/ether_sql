import os, stat
import pytest

from utils import get_process, wait_for_socket
from tests.fixtures.common import session_settings, drop_session_tables
from ether_sql.session import Session
from ether_sql.globals import push_session
from click.testing import CliRunner
from ether_sql.cli import cli
from web3 import Web3
from subprocess import call

DATADIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
    'parity-local-fixture'))

PARITY_FIXTURE = {
    'coinbase': 'dc544d1aa88ff8bbd2f2aec754b1f1e99e1812fd',
    'block_hash_with_log': '0x342e12ab6d24d7fb1d774a6b47cd2cc04430a3295bee5662d5a1a0b766480031',
    'block_with_txn_hash': '0xa866266a5a348948c38855cc6e990093b35a3d2c43fdddfe3b1259c9c3fc7404',
    'emitter_address': '0x4aA591a07989b4F810E2F5cE97e769D60710f168',
    'emitter_deploy_txn_hash': '0xa81e903e9953758c8da5aaae66451ff909edd7bd6aefc3ebeab1e709e3229bcc',
    'empty_block_hash': '0xbcb2826e4376c23e66750607af72965f177f93b39e5024be259e6b0ff4f95e9d',
    'math_address': '0xd794C821fCCFF5D96F5Db44af7e29977630A9dc2',
    'math_deploy_txn_hash': '0x03cc47c8f58608576187825aed01c4fc64786f1172d182d432336881a75a0fa3',
    'mined_txn_hash': '0x9839fde5fce7f0ed29b49a687d4f7630076069e65c2e1df87ffab9b2844d3899',
    'raw_txn_account': '0x39EEed73fb1D3855E90Cbd42f348b3D7b340aAA6',
    'txn_hash_with_log': '0x26bad3318b3466833f96d04ac9ba46fbbce11c15be2f83c9fe0b5dc15b2646cd'
}

PARITY_LOCAL_SETTINGS = "ParityLocalTestSettings"

@pytest.fixture(scope='module')
def ipc_path():
    _ipc_path = os.path.join(DATADIR, 'jsonrpc.ipc')
    yield _ipc_path

@pytest.fixture(scope="module")
def parity_import_blocks_command(ipc_path):
    return (
        'parity',
        'import', os.path.join(DATADIR, 'blocks_export.rlp'),
        '--chain', os.path.join(DATADIR, 'chain_config.json'),
        '--ipc-path', ipc_path,
        '--base-path', DATADIR,
        '--no-jsonrpc',
        '--no-ws',
        '--tracing', 'on',
    )

@pytest.fixture(scope="module")
def parity_import_blocks_process(parity_import_blocks_command):
    yield from get_process(parity_import_blocks_command, terminates=True)

@pytest.fixture(scope="module")
def parity_command_arguments(
    parity_import_blocks_process,
    ipc_path
):
    return (
        'parity',
        '--chain', os.path.join(DATADIR, 'chain_config.json'),
        '--ipc-path', ipc_path,
        '--base-path', DATADIR,
        '--no-jsonrpc',
        '--no-ws',
    )

@pytest.fixture(scope="module")
def parity_process(parity_command_arguments):
    yield from get_process(parity_command_arguments)

@pytest.yield_fixture(scope="module")
def parity_local_settings(parity_process, ipc_path):
    wait_for_socket(ipc_path)
    parity_settings = session_settings(setting_name=PARITY_LOCAL_SETTINGS)
    session = Session(PARITY_LOCAL_SETTINGS)
    push_session(session)
    yield PARITY_LOCAL_SETTINGS
    drop_session_tables(setting_name=PARITY_LOCAL_SETTINGS)

@pytest.fixture(scope="module")
def parity_push_blocks_in_sql(parity_local_settings):
    runner = CliRunner()
    runner.invoke(cli, ['--settings', parity_local_settings,
                        'scrape_block_range',
                        '--start_block_number', 1])
