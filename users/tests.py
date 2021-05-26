import json, jwt

from django.test   import Client, TestCase
from unittest.mock import patch, MagicMock

from users.models  import User
from my_settings   import SECRET

class KakaoLoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            social_login_id = "abcd1234",
            nickname        = "CREAM",
            email           = "cream@abc.com"
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_kakao_user_login_success_first_time(self, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                        "id"            : "abab1212",
                        "kakao_account" : {
                                            "email"   : 'teamcream@abc.com',
                                            "profile" : { 'nickname' : 'TeamCREAM' }
                        }
                    }
                    
        client = Client()
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        headers              = {"HTTP_AUTHORIZATION": "kakao_token"}
        response             = client.post("/users/kakao", **headers)

        user_id = User.objects.get(nickname="TeamCREAM").id
        cream_token = jwt.encode({'user_id': user_id}, SECRET, algorithm='HS256')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'cream_token': cream_token, 'user_id': user_id
        })
        
    @patch("users.views.requests")
    def test_kakao_user_login_success_not_first_time(self, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                        "id"            : "abcd1234",
                        "kakao_account" : {
                                            "email"   : 'cream@abc.com',
                                            "profile" : { 'nickname' : 'CREAM' }
                        }
                    }
                    
        client = Client()
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        headers              = {"HTTP_AUTHORIZATION": "kakao_token"}
        response             = client.post("/users/kakao", **headers)

        user_id = User.objects.get(nickname="CREAM").id
        cream_token = jwt.encode({'user_id': user_id}, SECRET, algorithm='HS256')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'cream_token': cream_token, 'user_id': user_id
        })

    @patch("users.views.requests")
    def test_kakao_user_login_access_token_required(self, request):
        client = Client()
        headers = {"HTTP_AUTHORIZATION": None}
        response = client.post("/users/kakao", **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'ACCESS_TOKEN_REQUIRED'})

    @patch("users.views.requests")
    def test_kakao_user_login_invalid_token(self, mocked_requests):
        class MockedResponse:
            def json(self):
                return None

        client = Client()
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        headers              = {"HTTP_AUTHORIZATION": "kakao_token"}
        response             = client.post("/users/kakao", **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'INVALID_TOKEN'})