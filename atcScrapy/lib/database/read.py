from atcScrapy.lib.database.connect import create_db_connection

def execute_db_query(query):

    db_connection = create_db_connection()
    db_cursor = db_connection.cursor(dictionary=True)

    db_cursor.execute(query)

    query_result = db_cursor.fetchall()

    db_connection.close()

    return query_result