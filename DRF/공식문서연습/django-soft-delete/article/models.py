from django.db import models
from django_softdelete.models import SoftDeleteModel


class Article(SoftDeleteModel):
    title = models.CharField(max_length=100)
    
    # Following fields will be added automatically
    # is_deleted
    # deleted_at