import db

def add_workout(title, description, duration, intensity, user_id):
    sql = """INSERT INTO workouts (title, description, duration, intensity, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql,[title, description, duration, intensity, user_id])

def get_workouts():
    sql = "SELECT id, title FROM workouts ORDER BY id DESC"
    return db.query(sql)

def get_workout(workout_id):
    sql = """SELECT workouts.id,
                    workouts.title,
                    workouts.description,
                    workouts.duration,
                    workouts.intensity,
                    users.id user_id,
                    users.username
            FROM workouts, users
            WHERE workouts.user_id = users.id AND
                workouts.id = ?"""
    return db.query(sql, [workout_id])[0]

def update_workout(workout_id, title, description, duration, intensity):
    sql = """UPDATE workouts SET title = ?,
                            description = ?,
                            duration = ?,
                            intensity = ?
                        WHERE id = ?"""
    db.execute(sql, [title, description, duration, intensity, workout_id])

def remove_workout(workout_id):
    sql = "DELETE FROM workouts WHERE id = ?"
    db.execute(sql, [workout_id])

def find_workouts(query):
    sql = """SELECT id, title
            FROM workouts
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY id DESC"""
    like = "%" + query +"%"
    return db.query(sql,  [like, like])