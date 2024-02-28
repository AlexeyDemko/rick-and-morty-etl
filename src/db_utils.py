from contextlib import contextmanager

import psycopg2


def get_db_conn():
    return psycopg2.connect(
        dbname="rick",
        user="rick",
        password="rick",
        host="db",
    )


@contextmanager
def db_connection():
    conn = get_db_conn()
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query, params=None):
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
