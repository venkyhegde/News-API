import bcrypt
from dao.user_service import UserService
from model.user_model import User


class Security:

    @staticmethod
    def authenticate(username, password):
        """
        Function to authenticate user
        :param username:
        :param password:
        :return:
        """
        user_service = UserService()
        user = user_service.find_by_username(username=username)
        if user and bcrypt.checkpw(password=password.encode('utf8'), hashed_password=user.password):
            user.password = password
            return user.json()
