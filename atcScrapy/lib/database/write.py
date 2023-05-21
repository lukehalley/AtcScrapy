from atcScrapy.lib.database.connect import create_db_connection

def execute_db_insert(query_table_name, query_keys, query_values, update_on_exists=True):

    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()

    query_keys_str = ",".join(query_keys)

    format_list = ['%s'] * len(query_keys)
    format_str = ",".join(format_list)

    query_str = f"""INTO {query_table_name} ({query_keys_str}) VALUES ({format_str})"""

    if update_on_exists:
        query_str = f"REPLACE {query_str}"
    else:
        query_str = f"INSERT {query_str}"

    db_cursor.execute(query_str, query_values)

    db_connection.commit()

    db_connection.close()

def execute_db_update(query_table_name, update_dict, where_dict):

    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()

    query = f"UPDATE " \
                 f"{query_table_name} " \
                 f"SET"

    for index, (key, value) in enumerate(update_dict.items()):
        query = f"{query} {query_table_name}.{key} = {value}"
        if index + 1 < len(update_dict):
            query = f"{query},"

    query = f"{query} " \
                 f"WHERE"

    for index, (key, value) in enumerate(where_dict.items()):
        query = f"{query} {key} = {value}"
        if index + 1 < len(update_dict):
            query = f"{query} AND"

    db_cursor.execute(query)

    db_connection.commit()

    db_connection.close()