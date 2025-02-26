from django.urls import path

from items.views import (
    buy_item,
    item_detail,
    ItemsListView,
    SuccessView,
)

app_name = 'items'

urlpatterns = [
    path('<int:id>/buy/', buy_item, name='buy_item'),
    path('<int:id>/', item_detail, name='item_detail'),

    path('', ItemsListView.as_view(), name='items_list'),
]