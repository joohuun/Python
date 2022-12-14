from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Person(models.Model):
    
    name = models.CharField(max_length=200)
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
