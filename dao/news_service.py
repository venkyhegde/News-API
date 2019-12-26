from model.news_model import News
from config.db_config import ConnectionPool
from typing import List


class NewsService:

    def __init__(self):
        self.__db = ConnectionPool.get_connection()

    def get_all_news(self):
        # get the collection
        news_collection = self.__db["news-content"]
        # find query to get all news (limit 100)
        result = news_collection.find().limit(100)
        # prepare news object and return
        news_list = list()
        for news in result:
            news_obj = self.__get_news_object(news)
            news_list.append(news_obj.json())
        if len(news_list) > 0:
            return news_list
        return None

    def publish_news(self, news: News):
        # get collection
        news_collection = self.__db["news-content"]
        # validate the news object
        is_valid = self.__validate_news(news)
        # insert news object
        if is_valid:
            _id = news_collection.insert_one(news.json()).inserted_id
        # get the news id and return the news id
        if _id is not None:
            return _id
        return None


    def __get_news_object(self, news) -> News:
        if news is not None:
            news_obj = News(_id=str(news["_id"]), category=news["category"], headline=news["headline"],
                            authors=news["authors"], link=news["link"], short_description=news["short_description"],
                            date=news["date"])
            return news_obj
        else:
            return None

    def __validate_news(self, news: News):
        is_valid: bool = True
        error_message = []
        # check for headline
        if news.headline is None or len(news.headline) < 4:
            is_valid = False
            error_message.append("Missing headline!")
        # check for category
        if news.category is None or len(news.category) <3:
            is_valid = False
            error_message.append("Missing news category!")
        # check for author
        if news.authors is None or len(news.authors) < 4:
            is_valid = False
            error_message.append("Missing author details!")
        # check for link
        if news.link is None or len(news.link) < 10:
            is_valid = False
            error_message.append("Missing link!")
        # check for short description
        if news.short_description is None or len(news.short_description) < 10:
            is_valid = False
            error_message.append("Missing description!")

        if is_valid is not True:
            raise ValueError(" ".join(error_message))
        else:
            return True


