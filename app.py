from flask import Flask
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

from config.db_config import ConnectionPool
from config.config import Config

from api.user_api import UserRegister, UserLogin
from api.news_api import NewsContent

app = Flask(__name__)

app.config["BUNDLE_ERRORS"] = True
app.secret_key = Config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
jwt = JWTManager(app)

api = Api(app)


db = ConnectionPool.get_connection()
news_content = db["news-content"]


class Test(Resource):
    def get(self):
        records = news_content.count_documents({})
        return {"records": records}

# Test api as heartbeat
api.add_resource(Test, "/test")

# user registration and login
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserLogin, "/auth/login")
# get all the news
api.add_resource(NewsContent, "/news/get-news", endpoint="get-news")
# posting / publishing a new news.
api.add_resource(NewsContent, "/news/publish", endpoint="publish")

if __name__ == "__main__":
    app.run(port=8080, debug=False)
