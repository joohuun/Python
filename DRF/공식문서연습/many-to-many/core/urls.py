from django.urls import path, include
from . import views
from . views import StudentsViewSet, ModulesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("student", StudentsViewSet, basename="student")
router.register("module", ModulesViewSet, basename="module")


urlpatterns = [ 
    path('asd', views.menu, name='menu'), 
    path('', include(router.urls)),
]