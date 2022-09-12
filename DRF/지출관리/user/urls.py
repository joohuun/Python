from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('/signup', views.SignupView.as_view(), name="signup_view"),
    path('/login', views.LoginView.as_view(), name="login_view"),
    path('/refresh', TokenRefreshView.as_view(), name="tokenrefresh_view"),
    path('/authonly', views.OnlyAuthenticatedUserView.as_view(), name="user_view"),
    path('/authonly/<int:pk>', views.OnlyAuthenticatedUserView.as_view()),
]