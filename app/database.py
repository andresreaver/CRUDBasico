import sqlite3

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row #Permite el acceso a las filas como un diccionario
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        create table if not exists users (
            id integer primary key autoincrement,
            name text not null,
            email text not null unique
        )
    """)
    conn.commit()
    conn.close()