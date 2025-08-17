CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE workouts(
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    duration INTEGER,
    user_id INTEGER REFERENCES users
);

CREATE TABLE workout_classes(
    id INTEGER PRIMARY KEY,
    workout_id INTEGER REFERENCES workouts,
    title TEXT,
    value TEXT
);