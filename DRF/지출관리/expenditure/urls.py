from django.urls import path
from .views import ExpenditureView, ExpenditureDeleteView, ExpenditureDetailView

urlpatterns = [
    path('', ExpenditureView.as_view(), name="expend_view"),
    path('/<int:pk>', ExpenditureView.as_view(), name="edit_delete_expend_view"),
    path('/soft-delete/<int:pk>', ExpenditureDeleteView.as_view(), name="edit_is_active"),
    path('/detail/<int:pk>', ExpenditureDetailView.as_view(), name="expendituredetail_view"),
]