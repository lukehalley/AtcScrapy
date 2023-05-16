from atcScrapy.lib.database.connect import create_db_connection


def execute_db_query(query_table_name, query_keys, query_values):

    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()

    query_keys_str = ",".join(query_keys)

    db_cursor.execute(f""" INSERT IGNORE INTO {query_table_name} ({query_keys_str}) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", list(query_values))

    db_connection.commit()

    db_connection.close()


