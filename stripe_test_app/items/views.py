from django.shortcuts import render

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
import stripe
from django.conf import settings
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_item(request, id):
    """получить Stripe Session Id для оплаты выбранного Item"""
    item = get_object_or_404(Item, id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'session_id': session.id})


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(
        request,
        'items/item_detail.html',
        {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    )


