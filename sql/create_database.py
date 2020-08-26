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

def create_burger(conn, burger): 
    """
    Create a new burger within the table 
    :param conn: 
    :param burger: 
    :return burger_id: 
    """ 
    sql_cmd = ''' INSERT INTO burgers(name, availability) 
                  VALUES(?,?) ''' 
    
    cursor = conn.cursor() 
    cursor.execute(sql_cmd, burger)
    return cursor.lastrowid 

def main(): 
    database = "sqldemo.db" 

    conn = create_connection(database) 
    with conn: 
        # Create burger table 
        burger_table_cmd = """ CREATE TABLE IF NOT EXISTS burgers (
        name text NOT NULL, 
        availability integer
    ); """

        create_table(conn, burger_table_cmd)

        # Create new burgers  
        bur1 = ("Classic Juicy Beef Burgs", 0) 
        bur2 = ("Southern Fried Chicken Burger", 0) 
        bur3 = ("Summer Sunset", 0) 
        bur4 = ("Baa-Baa Burger", 0) 
        bur5 = ("Premium Wagyu Burger", 0)

        create_burger(conn, bur1)
        create_burger(conn, bur2)
        create_burger(conn, bur3)
        create_burger(conn, bur4)
        create_burger(conn, bur5)

        conn.commit() 
        conn.close()

if __name__ == "__main__": 
    main()