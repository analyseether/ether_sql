from tests.common_tests.cli import (
    export_to_csv_single_thread,
    verify_block_contents,
)


class TestParityBlock56160():

    def test_parity_export_to_csv(self, parity_session_block_56160):
        export_to_csv_single_thread(parity_session_block_56160)
        pass

    def test_parity_verify_block_contents(self, parity_session_block_56160):
        verify_block_contents(parity_session_block_56160)
        pass
