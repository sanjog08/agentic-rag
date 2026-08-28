from app.resources import *
from app.models.chatMessages import chat_message_insert_one
from app.models.userThreads import user_thread_create
from app.graph.graph import chatbot
import uuid
import logging


logger = logging.getLogger(__name__)


class SendMessage(Resource):

    @authenticate()
    @exception_handler()
    def post(self, **kwargs):
        try:
            json_data = request.get_json(force=True)
            thread_id = json_data.get('thread_id')
            message = json_data.get('human_message')

            thread_id, get_chatbot_ans = self.send_message_to_bot(message, thread_id, **kwargs)
            data = {"thread_id": thread_id, "bot_reply": get_chatbot_ans}

            return responsify(body= data)
        except Exception as e:
            raise e

    @classmethod
    @exception_handler()
    def send_message_to_bot(cls, message, thread_id=None, **kwargs):

        user_id = "user-vip"

        if not message:
            return responsify(has_error= True, errors= "message is required.")

        if not thread_id:
            thread_id = uuid.uuid4().hex

            created = user_thread_create(user_id, thread_id)
            if not created:
                return responsify(has_error=True, errors="Thread creation failed, try again.")

        message_dict = {
            "thread_id": thread_id,
            "role": "user",
            "msg": message
        }

        message_insert = chat_message_insert_one(message_dict)
        if not message_insert:
            return responsify(has_error=True, errors="Problem in storing human message.")

        logger.error(f"human message is here: {message}")

        ai_response = chatbot.invoke({"thread_id": thread_id, "question": message})
        logger.error(f"AI response got API: {ai_response}")

        answer = ai_response.get('response')

        message_dict['role'] = "bot"
        message_dict['msg'] = answer

        message_insert = chat_message_insert_one(message_dict)
        if not message_insert:
            return responsify(has_error=True, errors="Problem in storing ai message.")

        return thread_id, answer