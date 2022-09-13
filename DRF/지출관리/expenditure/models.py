from django.db import models
from django.utils import timezone

# Create your models here.
class SoftDeleteManager(models.Manager):
    use_for_related_fields = True  # 옵션은 기본 매니저로 이 매니저를 정의한 모델이 있을 때 이 모델을 가리키는 모든 관계 참조에서 모델 매니저를 사용할 수 있도록 한다.

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    
    
class SoftDeleteModel(models.Model):
#    deleted_at = models.DateTimeField('삭제일', null=True, default=None)
   is_deleted = models.BooleanField("삭제여부", default=False)
   objects = SoftDeleteManager()  # 커스텀 매니저 

   class Meta:
       abstract = True  # 상속 할수 있게 

   def delete(self, *args, **kwargs):
       self.is_deleted == True
       self.save()
    #    self.deleted_at = timezone.now()
    #    self.save(update_fields=['deleted_at'])

   def restore(self,):  # 삭제된 레코드를 복구한다.
       self.is_deleted == False
       self.save
    #    self.deleted_at = None
    #    self.save(update_fields=['deleted_at'])


class Category(models.Model):
    TYPE = [
        ('0', "의"),
        ('1', "식"),
        ('2', "주"),
    ]
    type = models.CharField("카테고리", max_length=50, choices=TYPE)
    
    class Meta:
        db_table = '카테고리'


class Expenditure(SoftDeleteModel):
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