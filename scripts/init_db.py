#!/usr/bin/env python3
"""Initialize SQLite DB for Intramurals System.

Creates `data/intramurals.db`, applies the schema from `sql/schema.sql`,
sets recommended PRAGMAs, and seeds sample sports.
"""

import sqlite3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
DB_DIR = ROOT / "data"
DB_PATH = DB_DIR / "intramurals.db"
SCHEMA_FILE = ROOT / "sql" / "schema.sql"

def ensure_dirs():
    DB_DIR.mkdir(parents=True, exist_ok=True)

def initialize_db():
    if not SCHEMA_FILE.exists():
        print(f"Schema file not found: {SCHEMA_FILE}")
        sys.exit(1)

    ensure_dirs()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Recommended pragmas for durability and concurrency
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("PRAGMA synchronous = FULL;")
    cur.execute("PRAGMA foreign_keys = ON;")

    with SCHEMA_FILE.open("r", encoding="utf-8") as f:
        sql = f.read()
    cur.executescript(sql)
    conn.commit()

    # Seed sports if empty
    cur.execute("SELECT COUNT(*) AS c FROM sports;")
    c = cur.fetchone()[0]
    if c == 0:
        sample = [
            ("Basketball", "Boys/Girls"),
            ("Volleyball", "Boys/Girls"),
            ("Badminton", "Singles/Doubles"),
            ("Table Tennis", "Singles/Doubles"),
            ("Track & Field", "Open"),
            ("CODM", "E-Games"),
            ("Mobile Legends", "E-Games")
        ]
        cur.executemany("INSERT INTO sports (sport_name, category) VALUES (?, ?);", sample)
        conn.commit()
        print(f"Seeded {len(sample)} sports")
    else:
        print(f"Sports table already has {c} rows")

    # report counts
    for tbl in ("students", "sports", "teams", "student_sport"):
        cur.execute(f"SELECT COUNT(*) AS c FROM {tbl};")
        print(f"{tbl}:", cur.fetchone()[0])

    conn.close()
    print(f"Database created at: {DB_PATH}")

if __name__ == '__main__':
    initialize_db()
