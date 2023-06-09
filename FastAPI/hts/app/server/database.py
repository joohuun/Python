import motor.motor_asyncio
import pymongo

MONGO_DETAILS = "mongodb://root:root@localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.news

news_collection = database.get_collection("articles")



# # pymongo
# client = pymongo.MongoClient("mongodb://root:root@localhost:27017/admin")
# # news 데이터베이스를 생성합니다.
# db = client["news"]
# # articles 콜렉션을 생성합니다.
# col = db["articles"]

def article_helper(article) -> dict:
    return {
        "id": str(article["_id"]),
        "title": article["title"],
        "link": article["link"],
        "desc": article["desc"],
        "source": article["source"],
        "data": article["date"],
    }


async def retrieve_articles():
    articles = []
    async for article in news_collection.find():
        articles.append(article_helper(article))
        return articles