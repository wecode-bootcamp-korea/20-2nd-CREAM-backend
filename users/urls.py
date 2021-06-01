from django.urls import path
from users.views import KakaoLoginView, MyPageView

urlpatterns = [
    path('/kakao', KakaoLoginView.as_view()),
    path('/mypage', MyPageView.as_view())
]