from pymongo.errors import OperationFailure

from config.db_config import ConnectionPool
from model.user_model import User
import bcrypt
from bson.objectid import ObjectId


class UserService:

    def __init__(self):
        self.__db = ConnectionPool.get_connection()

    def find_by_username(self, username):
        """
        Method to find a user bu usr name
        :param username:
        :return:
        """
        # get the user collection
        user_collection = self.__db["user"]
        # find user
        user = user_collection.find_one({
            "username": username
        })

        if user:
            user = User(str(user["_id"]), user["username"], user["password"])
            return user
        else:
            user = None
        return user

    def find_by_id(self, _id):
        """
        Method to find a record by id
        :param _id:
        :return:
        """
        # get the user collection
        user_collection = self.__db["user"]
        user = user_collection.find_one({
            "_id": _id
        })
        if user:
            user = User(user["_id"], user["username"], user["password"])
            return user
        else:
            user = None
        return user

    def add_user(self, user_name, password):
        """
        Function to add new user to db
        :param user_name:
        :param password:
        :return:
        """
        # hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        # get user collection
        user_collection = self.__db["user"]
        # add insert_one to insert and get user id
        user = {
            "username": user_name,
            "password": hashed_password
        }
        user_new = User(_id=ObjectId(), username=user_name, password=hashed_password)
        try:
            _id = user_collection.insert_one(user_new.json()).inserted_id
        except OperationFailure:
            print("Access Denied")

        # check for user id is not none
        if str(_id) is not None:
            # create a user object
            user = User(str(_id), user_name, password)
            return user
        else:
            user = None
        return user

