from app.resources import *
from app.models.users import user_get_and_check_with_email, user_insert_one
from werkzeug.security import generate_password_hash, check_password_hash
import config
import jwt



class UserLogin(Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)

            email = json_data.get('email')
            password = json_data.get('password')

            if not email or not password:
                return responsify(has_error= True, errors= "email and password are required.")

            fetch_user = user_get_and_check_with_email(email=email, fetch_user=True)
            if fetch_user is None:
                return responsify(has_error=True, errors="user with this email not registered.")

            if not check_password_hash(fetch_user.get('password'), password):
                return responsify(has_error=True, errors="incorrect password, please check password.")

            session_valid_till = datetime.now() + timedelta(hours=2)
            session_timestamp = int(session_valid_till.timestamp())

            token_payload = {
                "name": fetch_user.get('name'),
                "email": fetch_user.get('email'),
                "token_validity": session_timestamp
            }

            jwt_token = jwt.encode(token_payload, config.JWT_SECRET, algorithm="HS256")
            data = {"message": "success", "jwt_token": jwt_token}

            return responsify(body=data)
            
        except Exception as e:
            raise e


class UserRegister(Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)
            
            name = json_data.get('name')
            email: str = json_data.get('email')
            password = json_data.get('password')

            if not name or not email or not password:
                return responsify(has_error= True, errors= "name, email and password are required.")

            check_user = user_get_and_check_with_email(email=email, check_user=True)
            if check_user:
                return responsify(has_error=True, errors="user with this email already registered, please login or use different email.")

            email = email.strip().lower()
            password = generate_password_hash(password)
            session_valid_till = datetime.now() + timedelta(hours=2)
            session_timestamp = int(session_valid_till.timestamp())

            user_dict = {
                "name": name,
                "email": email,
                "password": password
            }

            user_registration = user_insert_one(user_dict=user_dict)

            if user_registration:
                del user_dict['password']
                user_dict['token_validity'] = session_timestamp
            jwt_token = jwt.encode(user_dict, config.JWT_SECRET, algorithm="HS256")

            data = {"message": "success", "jwt_token": jwt_token}

            return responsify(body=data)

        except Exception as e:
            raise e