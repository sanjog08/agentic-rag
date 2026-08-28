from app.models import *

"""
Table name: user_threads
Having columns:
    id
    user_id
    thread_id
    created_at
"""



def user_thread_create(user_id, thread_id):
    if user_id and thread_id:
        query = "INSERT INTO user_threads (user_id, thread_id) VALUES (?, ?)"

        conn = turso_conn()
        conn.execute(query, (user_id, thread_id))
        conn.commit()

        conn.close()

        return True

    return False


def user_threads_single_user(user_id):
    if user_id:
        query = "SELECT * from user_threads where user_id = ?"

        conn = turso_conn()
        all_threads = conn.execute(query, (user_id, ))
        conn.close()

        threads = []
        for thread in all_threads:
            threads.append(thread[2])

        return threads

    return []


def user_threads_delete_single_user(user_id):
    if user_id:
        # need to impliment logic
        return True

    return False
