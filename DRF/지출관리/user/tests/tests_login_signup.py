from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User
# Create your tests here.

class SignupViewTest(APITestCase):
    """
    회원가입 테스트코드
    """
    def test_signup(self):
        url = reverse("signup_view")
        user_data = {
            "email":"test1@gmail.com",
            "password":"1234",
            "username":"테스트1" 
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 200)      
        
        
class LoginViewTest(APITestCase):
    """
    로그인 테스트코드
    """
    def setUp(self) -> None:
        self.data = {"email": "test1@gmail.com", "password": "test1"}
        self.user = User.objects.create_user(email="test1@gmail.com", username="테스트1")
        self.user.set_password("test1")
        self.user.save()

    def test_login(self):
        response = self.client.post(reverse("login_view"), self.data)
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_user_data(self):
        access_token = self.client.post(reverse("login_view"), self.data).data['access']
        print(access_token, "39")
        response = self.client.get(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION = f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.data['email'])
        