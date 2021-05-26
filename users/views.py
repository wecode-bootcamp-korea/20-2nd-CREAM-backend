import json, jwt, requests

from django.http   import JsonResponse
from django.views  import View

from users.models  import User
from my_settings   import SECRET

class KakaoLoginView(View):
    def post(self, request):
        access_token = request.headers.get("Authorization", None)
        if not access_token:
            return JsonResponse({'message': 'ACCESS_TOKEN_REQUIRED'}, status=401)
                
        headers      =({'Authorization' : f"Bearer {access_token}"})
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