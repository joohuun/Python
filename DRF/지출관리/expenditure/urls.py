from django.urls import path
from .views import ExpenditureView, ExpenditureSoftDeleteView, ExpenditureDetailView

urlpatterns = [
    path('', ExpenditureView.as_view(), name="get_post_expend_view"),
    path('/<int:pk>', ExpenditureView.as_view(), name="put_delete_expend_view"),
    path('/soft-delete/<int:pk>', ExpenditureSoftDeleteView.as_view(), name="softdelete_expend_view"),
    path('/details/<int:pk>', ExpenditureDetailView.as_view(), name="expendituredetail_view"),
]