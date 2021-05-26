from django.urls import path
from users.views import KakaoLoginView

urlpatterns = [
    path('/kakao',KakaoLoginView.as_view()),
]