from django.urls import path

from orders.views import buy_order, create_tax, order_detail

app_name = "orders"

urlpatterns = [
    path("<int:order_id>/buy/", buy_order, name="buy_order"),
    path("<int:order_id>/", order_detail, name="order_detail"),
    path("create_tax/", create_tax, name="create_tax"),
]
