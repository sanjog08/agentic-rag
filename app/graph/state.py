from typing import TypedDict
from langchain_core.messages import BaseMessage

class RagState(TypedDict):
    conversation_id: str

    question: str
    chat_history: list[BaseMessage]
    response: str