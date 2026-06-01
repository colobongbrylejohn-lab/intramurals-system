from flask import Flask, g, request, jsonify
from flask_cors import CORS
import sqlite3
from pathlib import Path
import os
from waitress import serve

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = os.environ.get('INTRAMURALS_DB') or str(ROOT / 'data' / 'intramurals.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON;')
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

static_dir = ROOT / 'intramurals-system'
app = Flask(__name__, static_folder=str(static_dir), static_url_path='')
CORS(app)
app.teardown_appcontext(close_connection)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/sports', methods=['GET'])
def list_sports():
    db = get_db()
    cur = db.execute('SELECT id, sport_name, category FROM sports ORDER BY sport_name;')
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

@app.route('/api/registrations', methods=['GET'])
def list_registrations():
    db = get_db()
    q = '''
    SELECT ss.id, s.student_name, s.student_number, sp.sport_name, ss.division, ss.course_year,
           ss.team_name, t.team_name AS assigned_team, ss.submitted, ss.registered_at
    FROM student_sport ss
    LEFT JOIN students s ON s.id = ss.student_id
    LEFT JOIN sports sp ON sp.id = ss.sport_id
    LEFT JOIN teams t ON t.id = ss.team_id
    ORDER BY ss.registered_at DESC
    '''
    cur = db.execute(q)
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

@app.route('/api/register', methods=['POST'])
def register():
    payload = request.get_json() or {}
    required = ('student_name', 'student_number', 'sport_id')
    if not all(k in payload for k in required):
        return jsonify({'error': 'missing student_name, student_number or sport_id'}), 400

    student_name = payload.get('student_name').strip()
    student_number = payload.get('student_number').strip()
    sport_id = int(payload.get('sport_id'))
    division = payload.get('division')
    course_year = payload.get('course_year')
    team_name = payload.get('team_name')
    team_id = payload.get('team_id')

    db = get_db()
    cur = db.cursor()

    # Ensure student exists (by student_number). If not, insert.
    cur.execute('SELECT id FROM students WHERE student_number = ?;', (student_number,))
    r = cur.fetchone()
    if r:
        student_id = r['id']
    else:
        cur.execute('INSERT INTO students (student_name, student_number) VALUES (?, ?);', (student_name, student_number))
        student_id = cur.lastrowid

    # Upsert student_sport (unique student_id, sport_id)
    # Use SQLite UPSERT syntax
    cur.execute('''
    INSERT INTO student_sport (student_id, sport_id, team_id, division, course_year, team_name, submitted)
    VALUES (?, ?, ?, ?, ?, ?, 1)
    ON CONFLICT(student_id, sport_id) DO UPDATE SET
      team_id = excluded.team_id,
      division = excluded.division,
      course_year = excluded.course_year,
      team_name = excluded.team_name,
      submitted = 1,
      registered_at = datetime('now','localtime')
    ;
    ''', (student_id, sport_id, team_id, division, course_year, team_name))

    db.commit()
    return jsonify({'ok': True, 'student_id': student_id}), 201

@app.route('/api/students', methods=['GET'])
def list_students():
    db = get_db()
    cur = db.execute('SELECT id, student_name, student_number FROM students ORDER BY student_name;')
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

@app.route('/api/student/login', methods=['POST'])
def login():
    payload = request.get_json() or {}
    required = ('student_number',)
    if not all(k in payload for k in required):
        return jsonify({'error': 'missing student_number'}), 400

    student_number = payload.get('student_number').strip()

    db = get_db()
    cur = db.execute('SELECT id, student_name FROM students WHERE student_number = ?;', (student_number,))
    r = cur.fetchone()
    if not r:
        return jsonify({'error': 'student not found'}), 404

    return jsonify({'ok': True, 'student_id': r['id'], 'student_name': r['student_name']}), 200

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    payload = request.get_json() or {}
    required = ('username', 'password')
    if not all(k in payload for k in required):
        return jsonify({'error': 'missing username or password'}), 400

    username = payload.get('username').strip()
    password = payload.get('password').strip()

    # Placeholder for admin login logic - replace with actual authentication
    if username == 'admin' and password == 'password':
        return jsonify({'ok': True, 'admin_id': 1, 'admin_name': 'Admin'}), 200
    else:
        return jsonify({'error': 'invalid credentials'}), 401


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('Using DB at:', DB_PATH)
    serve(app, host='0.0.0.0', port=port)