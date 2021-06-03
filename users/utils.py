import json, jwt

from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET

def login_confirm(original_function):

    def wrapper(self, request, product_id):
        try:
            token = request.headers.get("Authorization", None)
            if token:
                token_payload = jwt.decode(token, SECRET, algorithms='HS256')
                user          = User.objects.get(id=token_payload['user_id'])
                request.user  = user
                return original_function(self, request, product_id)
                
            return JsonResponse({'message': 'NEED_LOGIN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=401)
        
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_USER_ERROR'}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER_ERROR'}, status=401)

    return wrapper