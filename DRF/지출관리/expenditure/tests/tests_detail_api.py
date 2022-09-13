import json
from rest_framework.test import APITestCase, APIClient
from user.models import User
from expenditure.models import Category, Expenditure, ExpenditureDetail

# Create your tests here.
class ExpendCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = User.objects.create(username="test1", email="test1@gmail.com")
        cls.category = Category.objects.create(id=1)
        cls.get_expend_data = Expenditure.objects.create(user=cls.user_data, dec="점심식사", amount="5000", date="2000-01-01")
        cls.request_expend_data = {"category":"1", "dec":"request 지출내역", "amount":"10000", "date":"2022-09-01"}
        cls.get_detail_data = ExpenditureDetail.objects.create(user=cls.user_data, detail="상세내역", expenditure=cls.get_expend_data)
        cls.request_detail_data = {"detail":"request 상세내역"}
        
        
    def test_get_detail_list(self) -> None:
        """
        detailView의 get 함수를 검증하는 함수
        """
        client = APIClient()
        user = self.user_data
        user_detail = self.get_detail_data
        
        client.force_authenticate(user=user)
        url = "/expenditures/details/" + str(user_detail.id)
        
        response = client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
    
    def test_when_is_user_is_unauthenticated_in_get_detail_list(self) -> None:
        """
        detailView의 get 함수를 검증하는 함수
        case : 로그인하지 않은 사용자가 조회하는 경우
        """
        client = APIClient()
        
        user_detail = self.get_detail_data
        url = "/expenditures/details/" + str(user_detail.id)

        response = client.get(url)
        result = response.json()
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["detail"], "Authentication credentials were not provided.")
        
        
    def test_post_board_content(self) -> None:
        """
        detailView의 post 함수를 검증하는 함수
        """
        client = APIClient()
        user = self.user_data
        request_data = self.request_detail_data
        user_detail = self.get_detail_data
        
        
        client.force_authenticate(user=user)
        url = "/expenditures/details/" + str(user_detail.id)
        
        response = client.post(url, data=json.dumps(request_data), content_type="application/json")
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['detail'], 'request 상세내역')
        
        
        
    def test_put_board_content(self) -> None:
        """
        detailView의 put 함수를 검증하는 함수
        """
        client = APIClient()
        user = self.user_data
        user_detail = self.get_detail_data
        request_data = {"detail": "댓글 변경 하기"}

        client.force_authenticate(user=user)
        url = "/expenditures/details/" + str(user_detail.id)

        response = client.put(url, data=json.dumps(request_data), content_type="application/json")
        print(response, "86")

        # self.assertEqual(response.status_code, 200)
        
        
        
    def test_delete_board_content(self) -> None:
        """
        detailView의 delete 함수를 검증하는 함수 (데이터 삭제)
        """
        client = APIClient()
        user = self.user_data
        user_detail = self.get_detail_data

        
        client.force_authenticate(user=user)
        url = "/expenditures/details/" + str(user_detail.id)

        response = client.delete(url)
        result = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, "삭제 완료!!")
        
        
        
        
