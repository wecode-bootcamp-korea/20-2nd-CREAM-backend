from django.urls import path

from orders.views import BuyView, SellView

urlpatterns = [
    path("/buy/<int:product_id>", BuyView.as_view()),
    path("/sell/<int:product_id>", SellView.as_view()),
]