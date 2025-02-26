import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_order(request, order_id):
    """Получить Stripe Session Id для оплаты заказа с несколькими Item"""
    # TODO: Добавить services для лучшей читаемости кода
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

    # Параметры для Stripe Checkout
    checkout_params = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': request.build_absolute_uri('/success/'),
        'cancel_url': request.build_absolute_uri('/cancel/'),
    }

    # Добавляем скидку, если она есть
    if order.discount:
        checkout_params['discounts'] = [{
            # Создание купона (для скидок):
            #     Используйте Stripe API или панель управления Stripe для создания купона.
            #     Или создайте купон через API
            'coupon': order.discount.coupon_id,  # Используем coupon_id из Stripe
        }]

    # Добавляем налог, если он есть
    # TODO: Доделать фиксированный налог
    if order.tax:
        checkout_params['automatic_tax'] = {'enabled': True}
        checkout_params['tax_id_collection'] = {'enabled': True}
        # checkout_params['tax_rates'] = [order.tax.tax_id]  # Используем tax_id из Stripe

    # Создаем сессию оплаты в Stripe
    session = stripe.checkout.Session.create(**checkout_params)

    return JsonResponse({'session_id': session.id})



def order_detail(request, order_id):
    """Отобразить детали заказа"""
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        'orders/order_detail.html',
        {'order': order, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    )



def create_tax(request):
    """Создать налог в Stripe и сохранить его в базе данных"""
    tax = stripe.TaxRate.create(
        display_name="VAT",
        percentage=20.0,  # 20% налог
        inclusive=True,  # Налог добавляется к сумме
    )

    return HttpResponse(f"Тариф налога успешно создан: {tax.id}", status=200)