import db

def add_item(title, description, duration, intensity, user_id):
    sql = """INSERT INTO items (title, description, duration, intensity, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql,[title, description, duration, intensity, user_id])