import os
import sys
from typing import Optional

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()


class Db:
    _conn: Optional[psycopg.Connection] = None

    @classmethod
    def conn(cls) -> psycopg.Connection:
        if cls._conn and not cls._conn.closed:
            return cls._conn
        try:
            cls._conn = psycopg.connect(os.getenv("DATABASE_URL"), row_factory=dict_row)
        except psycopg.OperationalError:
            sys.exit("Could not connect to database.")

        return cls._conn

    @classmethod
    def cur(cls) -> psycopg.Cursor:
        return cls.conn().cursor()

    @classmethod
    def close(cls):
        if cls._conn and not cls._conn.closed:
            cls._conn.close()
        cls._conn = None

    def __init__(self) -> None:
        cur = Db.cur()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sheets(
              id text PRIMARY KEY,
              link text,
              title text,
              abc text,
              abc_link text,
              musicxml bytea,
              musicxml_link text,
              has_midi boolean DEFAULT false,
              midi_link text
            );
        """)
        Db.conn().commit()


if __name__ == "__main__":
    db = Db()
    cur = Db.cur()
    cur.execute('select 1 as one;')
    print(cur.fetchone())
    Db.close()
