from pymongo import MongoClient
import pymongo
from config.config import Config
import dns # required to connect srv


class ConnectionPool(object):
    __db = None

    def __init__(self):
        if ConnectionPool.__db is None:
            ConnectionPool.get_connection()
        else:
            # raise exception
            raise Exception("Existing DB connection")

    @staticmethod
    def get_connection() -> pymongo.database.Database:
        # if connection exists return same else
        if ConnectionPool.__db is None:
            # get client
            __client = MongoClient(Config.DB_URL)
            # get database
            ConnectionPool.__db = __client[Config.DB_1]
            return ConnectionPool.__db
        else:
            return ConnectionPool.__db

    @staticmethod
    def close_connection() -> None:
        if ConnectionPool.__db is not None:
            ConnectionPool.__db.close()
