from django.contrib import admin

from .models import Book, City, Person

# Register your models here.
admin.site.register(City)
admin.site.register(Person)
admin.site.register(Book)
