import stripe
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_order(request, order_id):
    """Получить Stripe Session Id для оплаты заказа с несколькими Item"""
    order = get_object_or_404(Order, id=order_id)

    # Создаем список товаров для передачи в Stripe
    line_items = []
    for order_item in order.items.all():
        item = order_item.item
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),  # Stripe требует сумму в центах
            },
            'quantity': order_item.quantity,
        })

    # Создаем сессию оплаты в Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return JsonResponse({'session_id': session.id})



def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        'orders/order_detail.html',
        {'order': order, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    )


