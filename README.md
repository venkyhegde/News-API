# News-API

A naive Flask Restful services

Service urls - 
http://127.0.0.1:8080/test (GET)

http://127.0.0.1:8080/auth/register (POST)
Expects username and password in the request body

http://127.0.0.1:8080/auth/login (POST)
Expects username and password in the request body

http://127.0.0.1:8080/news/get-news (GET)
http://127.0.0.1:8080/news/publish (POST)
Required properties to publish a news are category, headline, authors, link, short_description, and date
