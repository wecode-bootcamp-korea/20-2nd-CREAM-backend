from django.urls import path
from orders.views import BuyView

urlpatterns = [
    path("/buy/<int:product_id>", BuyView.as_view()),
]