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

        if UserModel.find_by_email(data["email"]):
            return {"message": "email is already used."}, 400

        if UserModel.find_by_username(data["username"]):
            return {"message": "username already exists."}, 400

        if data["password"] != data["password_confirmation"]:
            return {"message": "password and password_confirmation do not match."}, 400

        data.pop("password_confirmation")
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, _id):
        user = UserModel.find_by_id(_id)
        if not user:
            return {"message": "User not found"}
        return user.json(), 200

    @classmethod
    def delete(cls, _id):
        user = UserModel.find_by_id(_id)
        if not user:
            return {"message": "User not found"}
        user.delete_from_db()
        return {"message": "User deleted successfully."}


class UserLogin(Resource):
    def post(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("email", type=str, required=True, help="This field cannot be blank.")
        user_parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")
        data = user_parser.parse_args()

        user = UserModel.find_by_email(data["email"])
        if user and user.check_password(password=data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"message": "Invalid credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        return {"message": "Logout successful."}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)
        return {"access_token": new_token}, 200
