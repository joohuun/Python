from django.contrib import admin
from .models import Expenditure, ExpenditureDetail, Category

# Register your models here.
admin.site.register(Expenditure)
admin.site.register(ExpenditureDetail)
admin.site.register(Category)

