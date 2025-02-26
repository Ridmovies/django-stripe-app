from django.urls import path

from orders.views import order_detail, buy_order, create_tax

app_name = 'orders'

urlpatterns = [
    path('<int:order_id>/buy/', buy_order, name='buy_order'),
    path('<int:order_id>/', order_detail, name='order_detail'),
    path('create_tax/', create_tax, name='create_tax'),
]