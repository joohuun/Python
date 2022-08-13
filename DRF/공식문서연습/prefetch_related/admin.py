from django.contrib import admin

from .models import Pizza, Topping

# Register your models here.
admin.site.register(Topping)
admin.site.register(Pizza)
