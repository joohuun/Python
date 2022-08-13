# Create your models here.
from unicodedata import name
from django.db import models

class Topping(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )