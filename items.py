import db

def add_item(title, description, duration, intensity, user_id):
    sql = """INSERT INTO items (title, description, duration, intensity, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql,[title, description, duration, intensity, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.title,
                    items.description,
                    items.duration,
                    items.intensity,
                    users.username
            FROM items, users
            WHERE items.user_id = users.id AND
                items.id = ?"""
    return db.query(sql, [item_id])[0]