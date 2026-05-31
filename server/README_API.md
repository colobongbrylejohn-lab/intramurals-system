# Intramurals API

Start the Flask API (ensure dependencies installed):

```bash
python3 -m pip install -r server/requirements.txt
python3 server/app.py
```

Endpoints:
- `GET /api/sports` — list available sports
- `GET /api/students` — list students
- `GET /api/registrations` — list submitted registrations
- `POST /api/register` — submit a registration (JSON)

POST /api/register payload example:

```json
{
  "student_name": "John Doe",
  "student_number": "2026001",
  "sport_id": 1,
  "division": "Boys",
  "course_year": "BSCS-1",
  "team_name": "Alpha Squad"
}
```

The API uses the same SQLite DB file at `data/intramurals.db` by default. To override:

```bash
export INTRAMURALS_DB=/path/to/intramurals.db
python3 server/app.py
```
