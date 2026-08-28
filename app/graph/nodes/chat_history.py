from app.graph.nodes import *
from app.models.chatMessages import get_all_chat_message
import logging

logger = logging.getLogger(__name__)


def load_history(state: RagState) -> RagState:

    thread_id = state.get('thread_id')
    message_list = []

    chat_list = get_all_chat_message(thread_id=thread_id)
    if not chat_list:
        return {'chat_history': message_list}

    # need to load the chat history
    for chat in chat_list:
        if chat[2] == "user":
            message_list.append(HumanMessage(content=chat[3]))
        elif chat[2] == "bot":
            message_list.append(AIMessage(content=chat[3]))
        else:
            logger.warning(f"Unknown chat role: {chat[2]}")
            continue

    return {'chat_history': message_list}