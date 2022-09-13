from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    TYPE = [
        ('0', "의"),
        ('1', "식"),
        ('2', "주"),
    ]
    type = models.CharField("카테고리", max_length=50, choices=TYPE)
    
    class Meta:
        db_table = '카테고리'


class Expenditure(models.Model):
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    dec = models.TextField("설명")
    amount = models.IntegerField("금액")
    date = models.DateField("날짜")
    is_active = models.BooleanField("활성화 여부", default=True)

    class Meta:
        db_table = '지출'
        
        
class ExpenditureDetail(models.Model):
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.CASCADE, null=True)
    expenditure = models.ForeignKey(Expenditure, verbose_name="원글", on_delete=models.CASCADE, null=True)
    detail = models.TextField("세부 내용")

    class Meta:
        db_table = '세부내용'