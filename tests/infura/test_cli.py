from tests.common_tests.cli import (
    export_to_csv_single_thread,
    fail_on_wrong_setting_name
)


class TestInfuraCliBlock56160():

    def test_infura_export_to_csv(self, infura_settings):
        export_to_csv_single_thread()
        pass

def test_infura_fail_on_wrong_setting_name():
    fail_on_wrong_setting_name()
