from app.graph.nodes import *
from app.services.gemini import llm
import logging

logger = logging.getLogger(__name__)



def invoke_llm(state: RagState) -> RagState:

    question = state['question']

    response = llm.invoke(question)
    answer = response.content[0].get('text')
    logger.error(f"response generate by the llm: {answer}")


    return {'response': answer}
    