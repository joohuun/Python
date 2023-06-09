
import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from datetime import datetime
from pymongo import DESCENDING

app = FastAPI()
MONGO_URL="mongodb://root:root@localhost:27017/admin"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.test


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ArticleModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    link: str = Field(...)
    desc: str = Field(...)
    source: str = Field(...)
    date: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.now())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "제목입니다",
                "link": "https://n.news.naver.com",
                "desc": "요약내용입니다",
                "source": "출처",
                "date": "6분전",
            }
        }


@app.post("/", response_description="Add new article", response_model=ArticleModel)
async def create_article(article: ArticleModel = Body(...)):
    article = jsonable_encoder(article)
    new_article = await db["articles"].insert_one(article)
    created_article = await db["articles"].find_one({"_id": new_article.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_article)


@app.get(
    "/", response_description="List all articles", response_model=List[ArticleModel]
)
async def list_articles():
    articles = await db["articles"].find().sort("created_at", DESCENDING).to_list(100)
    return articles


