import json, jwt, requests

from django.http   import JsonResponse
from django.views  import View

from users.models  import User
from orders.models import SellingInformation, BuyingInformation
from users.utils   import login_confirm
from my_settings   import SECRET

class KakaoLoginView(View):
    def post(self, request):
        access_token = request.headers.get("Authorization", None)
        if not access_token:
            return JsonResponse({'message': 'ACCESS_TOKEN_REQUIRED'}, status=401)
                
        headers      = ({'Authorization' : f"Bearer {access_token}"})
        URL          = "https://kapi.kakao.com/v2/user/me"
        response     = requests.post(URL, headers=headers)
        user_data    = response.json()
        if not user_data:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
            
        user_id      = user_data.get('id')

        login_user, created = User.objects.get_or_create(
            social_login_id = user_id,
            nickname        = user_data['kakao_account']['profile'].get('nickname', None),
            email           = user_data['kakao_account'].get('email', None)
        )

        cream_token = jwt.encode({'user_id': login_user.id}, SECRET, algorithm='HS256')

        return JsonResponse({'cream_token': cream_token, 'user_id': login_user.id}, status = 200)

class MyPageView(View):
    @login_confirm
    def get(self, request):
        user                = request.user
        if not request.user:
            return JsonResponse({'message': 'NEED_LOGIN'}, status=401)

        selling_information = SellingInformation.objects.filter(user_id=user.id)
        buying_information  = BuyingInformation.objects.filter(user_id=user.id)

        result = [
            {
                "user_information" : {
                                        "user_id"       : user.id,
                                        "user_nickname" : user.nickname,
                                        "user_email"    : user.email,
                                        "user_point"    : user.point,
                },
                "sell_biddings"    : {
                                        "sell_all"        : len(selling_information),
                                        "sell_proceeding" : len(selling_information.filter(status_id=2)),
                                        "sell_finished"   : len(selling_information.filter(status_id=1))
                },
                "buy_biddings"     : {
                                        "buy_all"        : len(buying_information),
                                        "buy_proceeding" : len(buying_information.filter(status_id=2)),
                                        "buy_finished"   : len(buying_information.filter(status_id=1))
                }
            }
        ]

        return JsonResponse({'result': result}, status = 200)
