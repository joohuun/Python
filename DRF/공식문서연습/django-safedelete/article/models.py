from django.db import models
# from safedelete.models import SafeDeleteModel
# from safedelete.models import HARD_DELETE_NOCASCADE
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from safedelete import DELETED_VISIBLE_BY_PK
from safedelete.managers import SafeDeleteManager
# Create your models here.



class CustomSafeDeleteManager(SafeDeleteManager):
    _safedelete_visibility = DELETED_VISIBLE_BY_PK

class TimeStampedModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomSafeDeleteManager()
    class Meta:
        abstract = True
        ordering = ["created_at"]


class Article(SafeDeleteModel):
    name = models.CharField(max_length=100)


class Order(SafeDeleteModel):
    name = models.CharField(max_length=100)
    articles = models.ManyToManyField(Article)