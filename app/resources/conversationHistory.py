from app.resources import *
from app.models.userThreads import user_threads_check_threads
from app.models.chatMessages import get_all_chat_message



class ConversationHistory(Resource):
    """
    This API is used to return the chat history
    within a conversation by user and bot response.
    """

    @authenticate()
    @exception_handler()
    def get(self, **kwargs):
        args = request.args

        thread_id = args.get('thread_id')
        if not thread_id:
            return responsify(body= "thread_id not given in request.")

        user_id = kwargs.get('user_id')

        thread_exists = user_threads_check_threads(thread_id, user_id)
        if not thread_exists:
            return responsify(has_error=True, errors="requested thread is not belongs to the loggedin user")

        message_list = []

        chat_list = get_all_chat_message(thread_id=thread_id)
        if not chat_list:
            return responsify(body={"data": message_list})

        # need to load the chat history
        for chat in chat_list:
            if chat[2] == "user":
                message_list.append({"user": chat[3]})
            elif chat[2] == "bot":
                message_list.append({"bot": chat[3]})
            else:
                logger.warning(f"Unknown chat role: {chat[2]}")
                continue

        data = {"data": message_list}
        return responsify(body=data)