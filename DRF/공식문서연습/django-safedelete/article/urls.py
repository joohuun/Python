from django.urls import path, include
from article.views import SoftDeleteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('soft-delete/<int:pk>', SoftDeleteViewSet, basename='review') # 리뷰

urlpatterns = [
    path('', include(router.urls)),
]