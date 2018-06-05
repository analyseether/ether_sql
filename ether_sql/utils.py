import os
from sqlalchemy import MetaData


def export_to_csv(ether_sql_session, directory):
    """
    Export the data in the psql to a csv

    :param session ether_sql_session: ether_sql session
    :param str directory: Directory where the data should be exported
    """

    # create the directory is it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    metadata = MetaData(ether_sql_session.db_engine)
    metadata.reflect()
    conn = ether_sql_session.db_engine.raw_connection()
    cursor = conn.cursor()
    for _table_name in metadata.tables:
        dbcopy_to = open('{}/{}.csv'.format(directory, _table_name), 'wb')
        copy_sql = 'COPY {} TO STDOUT WITH CSV HEADER'.format(_table_name)

        cursor.copy_expert(copy_sql, dbcopy_to)

    conn.close()
