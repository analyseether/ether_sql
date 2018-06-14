from tests.common_tests.cli import (
    export_to_csv_single_thread,
    verify_block_contents,
    push_block_range_single_thread,
)


def test_infura_push_block_range(infura_settings):
    push_block_range_single_thread(infura_settings)
    pass


class TestInfuraBlock56160():

    def test_infura_export_to_csv(self, infura_session_block_56160):
        export_to_csv_single_thread(infura_session_block_56160)
        pass

    def test_infura_verify_block_contents(self, infura_session_block_56160):
        verify_block_contents(infura_session_block_56160)
        pass
