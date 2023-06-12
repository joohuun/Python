from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Article(BaseModel):
    title: Optional[str]
    link: Optional[str]
    desc: Optional[str]
    source: Optional[str]
    date: Optional[str]

    class Cofig:
        schema_extra = {
            "example": {
                "title": "제목입니다",
                "link": "https://n.news.naver.com",
                "desc": "요약내용입니다",
                "source": "출처",
                "date": "6분전",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}