from django.db import models
from ..account.models import User
from ..models import BaseModel
# Create your models here.

class Article(BaseModel):
    
    class Meta:
        db_table = "아티클"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=100)


class Like(BaseModel):
    class Meta:
        db_table = "좋아요"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Comment(BaseModel):
    class Meta:
        db_table = "댓글"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField()