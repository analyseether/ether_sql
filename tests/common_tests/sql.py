import logging
from click.testing import CliRunner
from ether_sql.cli import cli

logger = logging.getLogger(__name__)


def drop_upgrade_tables(settings):
    """
    Removes and recreates the tables in the database
    """
    runner = CliRunner()
    result = runner.invoke(cli, ['--settings', settings,
                           'sql', 'drop_tables'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['--settings', settings,
                           'sql', 'upgrade_tables'])
    assert result.exit_code == 0


def block_number(settings):
    runner = CliRunner()
    logger.debug("{}".format(settings))
    result = runner.invoke(cli, ['--settings', settings,
                           'sql', 'blocknumber'])
    logger.debug('{}'.format(result))
    assert result.exit_code == 0
