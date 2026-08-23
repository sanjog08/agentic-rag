from app.graph.nodes import *
from app.models.chatMessages import get_all_chat_message

def load_history(state: RagState) -> RagState:

    thread_id = state.get('thread_id')
    message_list = []

    chat_list = get_all_chat_message(thread_id=thread_id)
    if not chat_list:
        return {'chat_history': message_list}

    # need to load the chat history
    for chat in chat_list:
        if chat.role == "user":
            message_list.append(HumanMessage(content=chat.msg))
        elif chat.role == "ai":
            message_list.append(AIMessage(content=chat.msg))
        else:
            return None

    return {'chat_history': message_list}