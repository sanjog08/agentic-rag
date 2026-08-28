from app.models import *

"""
Table name: chat_messages
Having columns:
    id
    thread_id
    role
    msg
    create_at
""" 


def chat_message_insert_one(message_dict=None):
    if message_dict:
        thread_id = message_dict.get('thread_id')
        role = message_dict.get('role')
        msg = message_dict.get('msg')

        query = "INSERT INTO chat_messages (thread_id, role, msg) VALUES (?, ?, ?)"

        conn = turso_conn()
        conn.execute(query, (thread_id, role, msg))
        conn.commit()

        conn.close()

        return True

    return False

def get_all_chat_message(thread_id=None):
    if thread_id:
        query = "SELECT * FROM chat_messages WHERE thread_id = ?"

        conn = turso_conn()
        chat_messages = conn.execute(query, (thread_id, ))
        conn.close()

        if not chat_messages:
            return None

        return chat_messages


def delete_chat_messages(thread_id=None):
    if thread_id:
        query = "DELETE FROM chat_messages WHERE thread_id = ?"

        conn = turso_conn()
        conn.execute(query, (thread_id, ))
        conn.commit()

        conn.close()