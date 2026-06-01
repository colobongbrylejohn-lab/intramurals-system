-- Schema for Intramurals System (SQLite)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    student_number TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sport_name TEXT NOT NULL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    sport_id INTEGER NOT NULL,
    FOREIGN KEY (sport_id) REFERENCES sports(id) ON DELETE CASCADE
);

-- student_sport stores registrations/selections
CREATE TABLE IF NOT EXISTS student_sport (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    sport_id INTEGER NOT NULL,
    team_id INTEGER,
    division TEXT,
    course_year TEXT,
    team_name TEXT,
    submitted INTEGER DEFAULT 0,
    registered_at DATETIME DEFAULT (datetime('now','localtime')),
    UNIQUE(student_id, sport_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (sport_id) REFERENCES sports(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
);