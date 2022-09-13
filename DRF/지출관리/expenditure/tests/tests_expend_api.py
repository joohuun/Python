import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from user.models import User
from expenditure.models import Category, Expenditure

# Create your tests here.
class ExpendCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = User.objects.create(username="test1", email="test1@gmail.com")
        cls.category = Category.objects.create(id=1)
        cls.get_expend_data = Expenditure.objects.create(user=cls.user_data, dec="점심식사", amount="5000", date="2000-01-01")
        cls.request_expend_data = {"category":"1", "dec":"햄버거", "amount":"10000", "date":"2022-09-01"}
        
        
    def test_get_expenditure_list(self) -> None:
        client = APIClient()
        user = self.user_data
        
        client.force_authenticate(user=user)
        url = reverse("get_post_expend_view")
        
        response = client.get(url)
        result = response.json()
        
        for i in result:
            self.assertEqual(i["is_active"], True)
        self.assertEqual(response.status_code, 200)
        
    
    def test_when_is_user_is_unauthenticated_in_get_expenditure_list(self) -> None:
        """
        ExpenditureView의 get 함수를 검증하는 함수
        case : 로그인하지 않은 사용자가 조회하는 경우
        """
        client = APIClient()
        url = reverse("get_post_expend_view")
        
        response = client.get(url)
        result = response.json()
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["detail"], "Authentication credentials were not provided.")
        
        
    def test_post_expenditure_content(self) -> None:
        """
        ExpenditureView의 post 함수를 검증하는 함수
        """
        client = APIClient()
        user = self.user_data
        request_data = self.request_expend_data
        
        client.force_authenticate(user=user)
        url = reverse("get_post_expend_view")
        
        response = client.post(url, data=json.dumps(request_data), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        
        
    def test_put_expenditure_content(self) -> None:
        """
        ExpenditureView의 put 함수를 검증하는 함수 (부분 내용 수정)
        """
        client = APIClient()
        user = self.user_data
        user_expenditure = self.get_expend_data
        request_data = {"dec": "지출내역 변경하기"}

        client.force_authenticate(user=user)
        url = "/expenditures/" + str(user_expenditure.id)
        
        response = client.put(url, data=json.dumps(request_data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        
        
    def test_delete_expeditures_content(self) -> None:
        """
        ExpenditureView의 delete 함수를 검증하는 함수 (데이터 삭제)
        """
        client = APIClient()
        user = self.user_data
        user_expenditure = self.get_expend_data
        
        client.force_authenticate(user=user)
        url = "/expenditures/" + str(user_expenditure.id)
        
        response = client.delete(url)
        result = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, "삭제 완료!!")
        
        
    def test_soft_delete_expenditures_content(self) -> None:
        """
        ExpenditureSoftDeleteView의 Patch 함수를 검증하는 함수
        """
        client = APIClient()
        user = self.user_data
        user_expenditure = self.get_expend_data

        client.force_authenticate(user=user)
        url = "/expenditures/soft-delete/" + str(user_expenditure.id)
        
        response = client.patch(url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, "소프트 삭제 완료!!")
        
        
