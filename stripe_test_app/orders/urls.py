from django.urls import path

from items.views import (
    buy_item,
    item_detail,
    ItemsListView,
)
from orders.views import order_detail, buy_order

app_name = 'orders'

urlpatterns = [
    path('orders/<int:id>/buy/', buy_order, name='buy_order'),
    path('orders/<int:id>/', order_detail, name='order_detail'),
]