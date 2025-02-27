from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
import stripe
import markdown
from django.conf import settings
from django.views.generic import ListView, TemplateView

from .models import Item


class ItemsListView(ListView):
    model = Item
    template_name = "items/items_list.html"


class SuccessView(TemplateView):
    template_name = "items/success.html"


class IndexView(TemplateView):
    template_name = "items/index.html"


def buy_item(request, id):
    """получить Stripe Session Id для оплаты выбранного Item"""

    item = get_object_or_404(Item, id=id)
    currency = item.currency  # Текущая валюта
    if currency == "usd":
        stripe.api_key = settings.STRIPE_SECRET_KEY
    elif currency == "eur":
        stripe.api_key = settings.EUR_STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": item.currency,
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri("/success/"),
        cancel_url=request.build_absolute_uri("/cancel/"),
    )
    return JsonResponse({"session_id": session.id})


def create_payment_intent(request, id):
    """Создать Payment Intent для оплаты товара"""
    item = get_object_or_404(Item, id=id)

    # Выбираем ключи Stripe в зависимости от валюты товара
    currency = item.currency  # Текущая валюта
    if currency == "usd":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        publishable_key = settings.STRIPE_PUBLIC_KEY
    elif currency == "eur":
        stripe.api_key = settings.EUR_STRIPE_SECRET_KEY
        publishable_key = settings.EUR_STRIPE_PUBLIC_KEY

    try:
        # Создаем Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),  # Сумма в центах/евроцентах
            currency=currency,
            automatic_payment_methods={"enabled": True},
            metadata={
                "item_id": item.id,
                "item_name": item.name,
            },
        )
        return JsonResponse(
            {
                "clientSecret": intent.client_secret,  # Возвращаем client_secret для Stripe Elements
                "publishableKey": publishable_key,
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(
        request,
        "items/item_detail.html",
        {"item": item, "stripe_public_key": settings.STRIPE_PUBLIC_KEY},
    )


def intent_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(
        request,
        "items/intent_detail.html",
        {"item": item, "stripe_public_key": settings.STRIPE_PUBLIC_KEY},
    )


def readme_view(request):
    # Загружаем файл README.md
    with open("README.md", "r") as f:
        content = f.read()

    # Преобразуем Markdown в HTML
    html_content = markdown.markdown(content)

    context = {"readme": html_content}
    return render(request, "items/readme.html", context)
