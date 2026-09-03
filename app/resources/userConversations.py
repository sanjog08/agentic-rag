from app.resources import *
from app.models.userThreads import user_threads_single_user


class UserConversations(Resource):
    """
    This API returns all the threads of the conversation
    previously done by the user.
    """

    @authenticate()
    @exception_handler()
    def get(self, **kwargs):
        user_id = kwargs.get('user_id')
        if not user_id:
            responsify(has_error=True, errors="Can't find threads for the logged in user")

        threads_list = user_threads_single_user(user_id)
        if not threads_list:
            return responsify(body="User didn't have any converation yet.")

        return responsify(body= {"data": threads_list})