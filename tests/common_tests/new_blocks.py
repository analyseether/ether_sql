import time
import logging
from celery.result import AsyncResult
from click.testing import CliRunner
from ether_sql.cli import cli
from ether_sql.session import Session
from ether_sql.globals import get_current_session
from ether_sql.tasks.filters import (
    new_blocks,
    push_blocks_in_queue,
)
from ether_sql.models import (
        Blocks,
        Transactions,
        Receipts,
        Uncles,
        Logs,
        Traces,
        MetaInfo,
        StateDiff,
        StorageDiff,
        BlockTaskMeta,
)
from web3.utils.encoding import to_int, to_hex
from tests.fixtures.expected_data import EXPECTED_BLOCK_HASHES
from tests.common_tests.blocks import verify_block_56160_contents

logger = logging.getLogger(__name__)
BASE_BLOCK = 56160

def checking_filter_workers(worker):
    timeout = time.time() + 35
    for line in worker.stderr:
        try:
            assert line.find("ERROR") < 0
        except AssertionError:
            logger.debug(line)
            raise AssertionError

        if time.time() > timeout:
            worker.terminate()
            break

def put_initial_blocks_in_waiting():
    current_session = get_current_session()

    put_blocks = range(BASE_BLOCK, BASE_BLOCK + current_session.settings.BLOCK_LAG)
    for block_number in put_blocks:
        block_data = current_session.w3.eth.getBlock(block_number)
        block_hash = block_data['hash']
        BlockTaskMeta.add_block_task_meta(task_name='new_blocks',
                              state='WAITING',
                              block_number=block_number,
                              block_hash=to_hex(block_hash))
    verify_pushed_sql_contents()
    with current_session.db_session_scope():
        block_task_meta = current_session.db_session.query(BlockTaskMeta).first()
        assert block_task_meta.block_number == BASE_BLOCK
        assert block_task_meta.block_hash == EXPECTED_BLOCK_HASHES[BASE_BLOCK]
        assert block_task_meta.state == 'WAITING'


def push_initial_blocks_in_queue():
    current_session = get_current_session()
    push_blocks_in_queue()
    with current_session.db_session_scope():
        block_task_meta = current_session.db_session.query(BlockTaskMeta).first()
        assert block_task_meta.block_number == BASE_BLOCK
        assert block_task_meta.block_hash == EXPECTED_BLOCK_HASHES[BASE_BLOCK]
        assert block_task_meta.state == 'PENDING'

def verify_pushed_block_56160_contents():
    current_session = get_current_session()
    with current_session.db_session_scope():
        block_task_meta = current_session.db_session.query(BlockTaskMeta).first()
        task_id = block_task_meta.task_id
    task_completed = AsyncResult(task_id).get()
    verify_block_56160_contents()

def verify_pushed_sql_contents():
    current_session = get_current_session()
    with current_session.db_session_scope():
        assert current_session.db_session.query(Blocks).count() == 0
        assert current_session.db_session.query(Transactions).count() == 0
        assert current_session.db_session.query(Receipts).count() == 0
        assert current_session.db_session.query(Logs).count() == 0
        assert current_session.db_session.query(Uncles).count() == 0

        if current_session.settings.PARSE_TRACE:
            assert current_session.db_session.query(Traces).count() == 0

        if current_session.settings.PARSE_STATE_DIFF:
            assert current_session.db_session.query(StateDiff).count() == 0
            assert current_session.db_session.query(StorageDiff).count() == 0

        assert current_session.db_session.query(BlockTaskMeta).count() == \
            current_session.settings.BLOCK_LAG
