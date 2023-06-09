# from fastapi import FastAPI
# from pymongo import Connection
# from pymongo import MongoClient
# import pymongo
import uvicorn

# host 파일에 hostname 등록했을 경우 사용가능 아래3개 다사용가능
# client = MongoClient('mongodb://mongo1:27017,mongo2:27018,mongo3:27018/?replicaSet=fn-replicaset')
# client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=fn-replicaset')
# client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/?replicaSet=fn-replicaset')
# client = MongoClient('mongodb://fn_news_dev:fn_news_dev@10.3.1.1:27017,10.3.1.1:27018,10.3.1.1:27019/fn?replicaSet=fn-replicaset')

# client = MongoClient('mongodb://fn_news_dev:fn_news_dev@mongo1:27017,mongo2:27018,mongo3:27019/fn?replicaSet=fn-replicaset')
# client = MongoClient('mongodb://fn_news_dev:fn_news_dev@10.3.1.1:27017,10.3.1.1:27018,10.3.1.1:27019/fn?replicaSet=fn-replicaset')
# client = MongoClient("mongodb://fn_news_dev:fn_news_dev@10.3.1.1:27017/fn")


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)



