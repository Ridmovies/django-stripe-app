from django.urls import path

from items.views import (
    buy_item,
    item_detail,
    create_payment_intent,
    ItemsListView,
    intent_detail,
    readme_view,
    IndexView,
)

app_name = 'items'

urlpatterns = [
    path('buy/<int:id>/', buy_item, name='buy_item'),
    path('intent_buy/<int:id>/', create_payment_intent, name='intent_buy'),

    path('item/<int:id>/', item_detail, name='item_detail'),
    path('intent_item/<int:id>/', intent_detail, name='intent_detail'),

    path('readme/', readme_view, name='readme'),
    path('', IndexView.as_view(), name='index'),

    # path('', ItemsListView.as_view(), name='items_list'),
]