from django.db import models
from django_softdelete.models import SoftDeleteModel, SoftDeleteManager


class Article(SoftDeleteModel):
    title = models.CharField(max_length=100)
    
    # Following fields will be added automatically
    # is_deleted
    # deleted_at
    
    # Following managers will be added automatically
    # objects = SoftDeleteManager()
    # deleted_objects = DeletedManager()


# For inherited model

# class Post(SoftDeleteModel, SomeParentModelClass):
#     title = models.CharField(max_length=100)