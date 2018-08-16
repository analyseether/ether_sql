from tests.common_tests.cli import (
    export_to_csv_single_thread,
)


class TestParityCliBlock56160():

    def test_parity_export_to_csv(self, parity_settings):
        export_to_csv_single_thread()
        pass
