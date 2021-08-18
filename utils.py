import sqlite3
from sqlite3 import Error, Connection
from constants import CREATE_SERVER_TABLE

def create_db(file: str) -> Connection:
    conn = None
    try:
        conn = sqlite3.connect(f"./db/{file}")
        return conn
    except Error as e:
        print(e)

def create_server(file: str) -> Connection:
    conn = None
    try:
        conn = sqlite3.connect(f"./db/servers/{file}.db")
        conn.execute(CREATE_SERVER_TABLE)
        conn.commit()
        return conn
    except Error as e:
        print(e)