import os
from celery.utils.log import get_task_logger
from sqlalchemy import MetaData
from ether_sql.globals import get_current_session
from ether_sql.tasks.worker import app

logger = get_task_logger(__name__)


@app.task()
def export_to_csv(directory='.'):
    """
    Export the data in the psql to a csv

    :param session ether_sql_session: ether_sql session
    :param str directory: Directory where the data should be exported
    """

    current_session = get_current_session()
    # create the directory is it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    metadata = MetaData(current_session.db_engine)
    metadata.reflect()
    conn = current_session.db_engine.raw_connection()
    cursor = conn.cursor()
    for _table_name in metadata.tables:
        dbcopy_to = open('{}/{}.csv'.format(directory, _table_name), 'wb')
        copy_sql = 'COPY {} TO STDOUT WITH CSV HEADER'.format(_table_name)

        cursor.copy_expert(copy_sql, dbcopy_to)
        logger.debug('exported table {}'.format(_table_name))

    conn.close()
