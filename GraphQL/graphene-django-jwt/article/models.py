from django.db import models

# Create your models here.

class Article(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    dec = models.TextField()

    class Meta:
        db_table = "아티클"

    def __str__(self):
        return self.title