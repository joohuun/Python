from typing import Optional
from pydantic import BaseModel, EmailStr, Field

"""
몽고디비에 저장될 디비 스키마 정의
스키마는 보낼 데이터 유형과 보내는 방법 정의
"""

class StudentSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "test1",
                "email": "test1@example.com",
                "year": "2",
                "gpa": "2.99"
            }
        }

class UpdateStudentModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    year: Optional[int]
    gpa: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "test1",
                "email": "test1@example.com",
                "year": "2",
                "gpa": "2.99"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code, 
        "message": message
    }
