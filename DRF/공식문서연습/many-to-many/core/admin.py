from django.contrib import admin
from . models import Menu, MenuOptinType, Modules, Students

# Register your models here.
admin.site.register(MenuOptinType)
admin.site.register(Menu)
admin.site.register(Modules)
admin.site.register(Students)

