from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from menulisulasan.models.user import UserModel
from menulisulasan import logger
from menulisulasan.resources import constant
from datetime import timedelta
from blacklist import BLACKLIST


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user = UserModel.find_by_id(get_jwt_identity())
        logger.info(user)
        if not user:
            return {"message": "User not found."}, constant.CODE_NOT_FOUND
        return user.json(), constant.CODE_OK

    @classmethod
    @jwt_required
    def delete(cls):
        user = UserModel.find_by_id(get_jwt_identity())
        logger.info(user)
        if not user:
            return {"message": "User not found."}, constant.CODE_NOT_FOUND
        user.delete_from_db()
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "User deleted successfully."}, constant.CODE_OK

    @classmethod
    @jwt_required
    def put(cls):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("id", type=int, required=True, help="This field cannot be blank.")
        user_parser.add_argument("first_name", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("last_name", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("email", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("username", type=str, required=True, help="This field cannot be blank.")
        data = user_parser.parse_args()
        logger.info(data)

        user = UserModel.find_by_id(get_jwt_identity())
        logger.info(user)

        if not user:
            return {"message": "User not found."}, constant.CODE_NOT_FOUND
        if data["id"] != get_jwt_identity():
            return {"message": "Not authorized."}, constant.CODE_UNAUTHORIZED
        if data["email"] != user.email and UserModel.find_by_email(data["email"]):
            return {"message": "Email is already used."}, constant.CODE_BAD_REQUEST
        if data["username"] != user.username and UserModel.find_by_username(data["username"]):
            return {"message": "Username already exists."}, constant.CODE_BAD_REQUEST

        data.pop("id")
        user.update_data_to_db(**data)
        return {"message": "User updated successfully."}, constant.CODE_OK


class UserRegistration(Resource):
    def post(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("first_name", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("last_name", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("email", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("username", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("password_confirmation", type=str, required=True, help="This field cannot be blank.")
        data = user_parser.parse_args()
        logger.info(data)

        if UserModel.find_by_email(data["email"]):
            return {"message": "Email is already used."}, constant.CODE_BAD_REQUEST
        if UserModel.find_by_username(data["username"]):
            return {"message": "Username already exists."}, constant.CODE_BAD_REQUEST
        if data["password"] != data["password_confirmation"]:
            return {"message": "Password does not match with Password Confirmation."}, constant.CODE_BAD_REQUEST

        data.pop("password_confirmation")
        user = UserModel(**data)
        user.save_to_db()
        logger.info(user)

        return {"message": "Registration successful."}, constant.CODE_CREATED


class UserLogin(Resource):
    def post(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("email", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")
        data = user_parser.parse_args()
        logger.info(data)

        user = UserModel.find_by_email(data["email"])
        logger.info(user)
        if user and user.check_password(password=data["password"]):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=365), fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "message": "Login successful.",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.json()
            }, constant.CODE_OK

        return {"message": "Invalid credentials!"}, constant.CODE_UNAUTHORIZED


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Logout successful."}, constant.CODE_OK


class UserChangePassword(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("id", type=int, required=True, help="This field cannot be blank.")
        user_parser.add_argument("current_password", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("new_password", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("new_password_confirmation", type=str, required=True,
                                 help="This field cannot be blank.")
        data = user_parser.parse_args()
        logger.info(data)

        user = UserModel.find_by_id(get_jwt_identity())
        logger.info(user)

        if not user:
            return {"message": "User not found."}, constant.CODE_NOT_FOUND
        if data["id"] != get_jwt_identity():
            return {"message": "Not authorized."}, constant.CODE_UNAUTHORIZED
        if not user.check_password(password=data["current_password"]):
            return {"message": "Wrong password."}, constant.CODE_UNAUTHORIZED
        if user.check_password(password=data["new_password"]):
            return {"message": "New password cannot be same with current password."}, constant.CODE_BAD_REQUEST
        if data["new_password"] != data["new_password_confirmation"]:
            return {"message": "New Password does not match with New Password Confirmation."}, constant.CODE_BAD_REQUEST

        user.update_password_to_db(data["new_password"])
        return {"message": "Password updated successfully."}, constant.CODE_OK


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)
        return {"access_token": new_token}, constant.CODE_OK
