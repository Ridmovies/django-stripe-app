from django.urls import path

from items.views import (
    buy_item,
    item_detail,
    ItemsListView,
)
from orders.views import order_detail, buy_order

app_name = 'orders'

urlpatterns = [
    path('<int:order_id>/buy/', buy_order, name='buy_order'),
    path('<int:order_id>/', order_detail, name='order_detail'),
]