from fastapi import FastAPI
from app.server.routes.article import (
    router as ArticleRouter,
    router
)
# from app.server.routes import  article
from app.server import database

app = FastAPI()

app.include_router(ArticleRouter, tags=["Article"], prefix="/article")

# router = APIRouter()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@router.get("/", response_description="Articles retrieved")
async def get_articles():
    articles = await database.retrieve_articles()
    if articles:
        return Res

