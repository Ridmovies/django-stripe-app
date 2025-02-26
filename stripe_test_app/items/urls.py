from django.urls import path

from items.views import (
    buy_item,
    item_detail,
    ItemsListView,
)

app_name = 'items'

urlpatterns = [
    path('buy/<int:id>/', buy_item, name='buy_item'),
    path('item/<int:id>/', item_detail, name='item_detail'),
    # path('', ItemsListView.as_view(), name='items_list'),
]