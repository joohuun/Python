
import pytest
from graphene.test import Client

from project.article.models import Article, Comment, Like
from project.account.models import User
from project.graphql.api import schema


client = Client(schema)


@pytest.mark.django_db
def test_resolve_all_article():
    user = User.objects.create(email="test1@gmail.com")
    Article.objects.create(user=user, title="안녕", body="하세요")
    Article.objects.create(user=user, title="안녕하", body="세요")

    query = """
        query {
            allArticles {
                id
                title
                body
            }
        }
    """
    result = client.execute(query)
    # print(client)
    print(result["data"]["allArticles"])      
    assert result == {
    "data": {
        "allArticles": [
            {
                "id": "1",
                "title": "안녕",
                "body": "하세요"
            },
            {
                "id": "2",
                "title": "안녕하",
                "body": "세요"
            }
            ]
        }
    }
    assert 'errors' not in result


@pytest.mark.django_db
def test_article_detail():
    user = User.objects.create(email="test1@gmail.com")
    article = Article.objects.create(id=1, user=user, title="안녕", body="하세요")
    Comment.objects.create(id=1, user=user, article=article, body="댓글")
    Comment.objects.create(id=2, user=user, article=article, body="댓글2")
    Like.objects.create(id=1, user=user, article=article)

    query = """
        query {
            articleDetail (id: 1) {
                id
                title
                body

                likeSet {
                id
                }

                commentSet {
                    id
                    body
                } 
        } 
    }
    """
    result = client.execute(query)
    assert result == {
    "data": {
        "articleDetail": {
            "id": "1",
            "title": "안녕",
            "body": "하세요",
            "likeSet": [
                {
                    "id": "1"
                }
            ],
            "commentSet": [
                {
                    "id": "1",
                    "body": "댓글"
                },
                {
                    "id": "2",
                    "body": "댓글2"
                },
            ]
        }
    }
}