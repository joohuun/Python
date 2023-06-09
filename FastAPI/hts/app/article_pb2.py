# article_pb2.py

import datetime

import grpc
import article_pb2
import article_pb2_grpc
from main import ArticleModel as Article

from pymongo import DESCENDING, MongoClient


class ArticleServicer(article_pb2_grpc.ArticleServiceServicer):
    def ListArticles(self, request, context):
        client = MongoClient("mongodb://root:root@localhost:27017/admin")
        db = client["test"]
        articles = db["articles"].find().sort("created_at", DESCENDING)
        
        for article in articles:
            article_pb = article_pb2.Article(
                id=str(article["_id"]),
                title=article["title"],
                link=article["link"],
                desc=article["desc"],
                source=article["source"],
                date=datetime.datetime.fromisoformat(article["date"]),
                created_at=datetime.datetime.fromisoformat(article["created_at"]),
            )
            yield article_pb


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    article_pb2_grpc.add_ArticleServiceServicer_to_server(ArticleServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
