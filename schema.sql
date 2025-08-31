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

CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    workout_id INTEGER REFERENCES workouts,
    evaluation INTEGER
);

CREATE TABLE classes(
    id INTEGER PRIMARY KEY,
    title TEXT,CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    workout_id INTEGER REFERENCES workouts,
    evaluation INTEGER
);
    value TEXT
);

CREATE TABLE workout_classes(
    id INTEGER PRIMARY KEY,
    workout_id INTEGER REFERENCES workouts,
    title TEXT,
    value TEXT
);