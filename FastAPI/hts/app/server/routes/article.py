from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder


from app.server.database import (
    retrieve_articles,
)

from app.server.models.article import (
    ErrorResponseModel,
    ResponseModel,
    Article,
)

router = APIRouter()