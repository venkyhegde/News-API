from flask_restful import Resource, reqparse
from dao.user_service import UserService
from config.api_config.security import Security

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)


class UserRegister(Resource):
    """
    User registration service
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username", type=str, required=True, help="Username can't be blank")
        self.parser.add_argument("password", type=str, required=True, help="Password can't be blank")
        super(UserRegister, self).__init__()

    def post(self):
        data = self.parser.parse_args()

        # get data from request
        user_name = data["username"]
        password = data["password"]
        # check if user already exists
        user_service = UserService()  # creating user service instance
        user = user_service.find_by_username(username=user_name)

        if user:
            msg = f"User with user name {user_name} already exists"
            return {"message": msg}, 400

        # otherwise insert user into database
        user = user_service.add_user(user_name, password)
        if user is None:
            return {"message": "Internal Server Error!"}, 500
        # print(user)
        return {"message": "Registration Successful", "user": user.json()}, 201


class UserLogin(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username", type=str, required=True, help="Username can't be blank")
        self.parser.add_argument("password", type=str, required=True, help="Password can't be blank")
        super(UserLogin, self).__init__()

    def post(self):
        data = self.parser.parse_args()

        # get data from request
        user_name = data["username"]
        password = data["password"]

        user = Security.authenticate(username=user_name,password=password)
        if user is None:
            return {"message": "Invalid username password"}, 401

        access_token = create_access_token(identity=user_name)
        return {"message": "login success!", "access_token": access_token, "user": user}, 200

