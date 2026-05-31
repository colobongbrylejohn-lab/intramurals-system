Intramurals System — SQLite DB initializer

Files added:
- `sql/schema.sql` — database schema (students, sports, teams, student_sport)
- `scripts/init_db.py` — creates `data/intramurals.db` and seeds sample sports

Usage:

Run the initializer (requires Python 3):

```bash
python3 scripts/init_db.py
```

The script creates `data/intramurals.db`. Ensure the `data/` directory is on persistent storage.
