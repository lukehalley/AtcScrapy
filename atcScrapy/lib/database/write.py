from atcScrapy.lib.database.connect import create_db_connection


def execute_db_insert(query_table_name, query_keys, query_values, update_on_exists=True):

    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()

    query_keys = ",".join(query_keys)

    query_str = f"""INTO {query_table_name} ({query_keys}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    if update_on_exists:
        query_str = f"REPLACE {query_str}"
    else:
        query_str = f"INSERT {query_str}"

    db_cursor.execute(query_str, query_values)

    db_connection.commit()

    db_connection.close()