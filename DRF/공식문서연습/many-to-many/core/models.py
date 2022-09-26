from django.db import models

# Create your models here.
class MenuOptinType(models.Model): # Routine
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    

class Menu(models.Model): # Routineday
    branch_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    option = models.ManyToManyField(MenuOptinType)
    
    
# https://github.com/CodeEnvironment/django-rest-framework-code/blob/master/school/api/views.py

class Modules(models.Model): # 루틴
    module_name = models.CharField(max_length=50)
    module_duaration = models.IntegerField()
    class_room = models.IntegerField()

    def __str__(self):
        return self.module_name


class Students(models.Model): # 루틴데이
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.IntegerField()
    modules = models.ManyToManyField(Modules, related_name="modules")

    def __str__(self):
        return self.name
