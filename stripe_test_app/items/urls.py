from django.urls import path

from items.views import (
    buy_item,
    create_payment_intent,
    intent_detail,
    item_detail,
    readme_view,
)

app_name = "items"

urlpatterns = [
    path("buy/<int:id>/", buy_item, name="buy_item"),
    path("intent_buy/<int:id>/", create_payment_intent, name="intent_buy"),
    path("item/<int:id>/", item_detail, name="item_detail"),
    path("intent_item/<int:id>/", intent_detail, name="intent_detail"),
    path("", readme_view, name="readme"),
]
