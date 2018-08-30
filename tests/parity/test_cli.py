from tests.common_tests.cli import (
    export_to_csv_single_thread,
    fail_on_wrong_setting_name
)


class TestParityCliBlock56160():

    def test_parity_export_to_csv(self, parity_settings):
        export_to_csv_single_thread()
        pass

def test_parity_fail_on_wrong_setting_name():
    fail_on_wrong_setting_name()
