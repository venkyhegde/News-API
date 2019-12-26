from flask_restful import Resource, reqparse
from bson.objectid import ObjectId

from dao.news_service import NewsService
from model.news_model import News


class NewsContent(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("category", type=str, required=True, help="category can't be blank")
        self.parser.add_argument("headline", type=str, required=True, help="headline can't be blank")
        self.parser.add_argument("authors", type=str, required=True, help="authors can't be blank")
        self.parser.add_argument("link", type=str, required=True, help="link can't be blank")
        self.parser.add_argument("short_description", type=str, required=True, help="short_description can't be blank")
        self.parser.add_argument("date", type=str, required=True, help="date can't be blank")
        self.news_service = NewsService() # create an instance of news service
        super(NewsContent, self).__init__()

    def get(self):
        # get the list of news object
        news_list = self.news_service.get_all_news()
        # return the news object
        if news_list is None:
            return {"message": "Internal Server Error"}, 500
        return {"news": news_list}, 200

    def post(self):
        # get the requests and create a news object
        data = self.parser.parse_args()
        print(data)
        news_obj = News(_id=ObjectId(), category=data["category"], headline=data["headline"],authors=data["authors"],
                        link=data["link"], short_description=data["short_description"], date=data["date"])
        # create a service object and call service method.
        inserted_id = self.news_service.publish_news(news_obj)
        if inserted_id is None:
            return {"message": "Internal Server error"}, 500
        return {"message": "Inserted successfully.", "_id": str(inserted_id)}