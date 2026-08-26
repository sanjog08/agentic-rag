from app.models import *

"""
Table name: users
Having columns:
    id
    name
    email
    password
    create_at
""" 

"""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def user_get_and_check_with_email(email=None, check_user=False, fetch_user=False):
    try:
        if email:
            query = "SELECT * FROM users WHERE email = ?"

            conn = turso_conn()
            user = conn.execute(query, (email,))
            user = user.fetchone()
            conn.close()

            if user and fetch_user:
                user_dict = {
                    "name": user[1],
                    "email": user[2],
                    "password": user[3]
                }
                return user_dict
            elif user and check_user:
                return True
            else:
                return {} if fetch_user else False

        return {} if fetch_user else False

    except Exception as e:
        print(f"this si the error ---------> {e}")
        # raise e


def user_insert_one(user_dict=None):
    if user_dict:
        name = user_dict.get('name')
        email = user_dict.get('email')
        password = user_dict.get('password')

        query = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
        
        conn = turso_conn()
        conn.execute(query, (name, email, password))
        conn.commit()

        conn.close()

        return True

    return False


def get_all_users():
    conn = turso_conn()
    users = conn.execute("SELECT * FROM users")
    conn.close()

    if not users:
        return None

    return users