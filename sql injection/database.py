import sqlite3
from sqlite3 import Error 

def create_connection(db_file): 
    try: 
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e: 
        print(e) 

    print("Returned None!@")
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def execute_query(conn, execute_query):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(execute_query)
    except Error as e:
        print(e)


conn = create_connection(":memory:") 
create_table(conn, """ CREATE TABLE IF NOT EXISTS users (
name TEXT NOT NULL, 
password TEXT NOT NULL
); """
)

execute_query(conn, """
INSERT INTO users (name, password) VALUES ();
""")

conn.commit() 
