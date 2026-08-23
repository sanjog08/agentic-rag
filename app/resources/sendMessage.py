from app.resources import *
from app.models.chatMessages import chat_message_insert_one
from app.graph.graph import chatbot
import uuid
import logging


logger = logging.getLogger(__name__)


class SendMessage(Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)
            thread_id = json_data.get('thread_id')
            message = json_data.get('human_message')

            get_chatbot_ans = self.send_message_to_bot(message, thread_id)

            return responsify(body= get_chatbot_ans)
        except Exception as e:
            raise e

    @classmethod
    def send_message_to_bot(cls, message, thread_id=None):

        if not message:
            return responsify(has_error= True, errors= "message is required.")

        if not thread_id:
            thread_id = uuid.uuid4().hex

        user_id = "user-1"

        message_dict = {
            "thread_id": thread_id,
            "role": "user",
            "msg": message,
            "create_at": datetime.now()
        }

        # message_insert = chat_message_insert_one(message_dict)

        # if not message_insert:
        #     return responsify(has_error=True, errors="Problem in storing human message.")

        logger.error(f"human message is here: {message}")

        ai_response = chatbot.invoke({"thread_id": thread_id, "question": message})
        logger.error(f"AI response got API: {ai_response}")

        answer = ai_response.get('response')

        return answer