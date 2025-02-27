import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .models import Tax

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Order
from .services.order_service import OrderService
from .services.stripe_service import StripeService


def buy_order(request, order_id):
    """Получить Stripe Session Id для оплаты заказа с несколькими Item"""
    order = get_object_or_404(Order, id=order_id)

    # Получаем список товаров для Stripe Checkout
    line_items = OrderService.get_line_items_for_order(order)

    # Создаем Stripe Checkout Session
    session = StripeService.create_checkout_session(
        line_items=line_items,
        success_url=request.build_absolute_uri("/success/"),
        cancel_url=request.build_absolute_uri("/cancel/"),
        discount=order.discount,
        tax=order.tax,
    )

    return JsonResponse({"session_id": session.id})


# def buy_order(request, order_id):
#     """Получить Stripe Session Id для оплаты заказа с несколькими Item"""
#     order = get_object_or_404(Order, id=order_id)
#
#     # Создаем список товаров для передачи в Stripe
#     line_items = []
#     for order_item in order.items.all():
#         item = order_item.item
#         line_item = {
#             'price_data': {
#                 'currency': item.currency,
#                 'product_data': {
#                     'name': item.name,
#                     'description': item.description,
#                 },
#                 'unit_amount': int(item.price * 100),  # Stripe требует сумму в центах
#             },
#             'quantity': order_item.quantity,
#         }
#
#         # Добавляем налоговую ставку к каждому товару, если она есть
#         if order.tax:
#             line_item['tax_rates'] = [order.tax.tax_id]  # Используем tax_id из Stripe
#
#         line_items.append(line_item)
#
#     # Параметры для Stripe Checkout
#     checkout_params = {
#         'payment_method_types': ['card'],
#         'line_items': line_items,
#         'mode': 'payment',
#         'success_url': request.build_absolute_uri('/success/'),
#         'cancel_url': request.build_absolute_uri('/cancel/'),
#     }
#
#     # Добавляем скидку, если она есть
#     if order.discount:
#         checkout_params['discounts'] = [{
#             # Создание купона (для скидок):
#             #     Используйте Stripe API или панель управления Stripe для создания купона.
#             #     Или создайте купон через API
#             'coupon': order.discount.coupon_id,  # Используем coupon_id из Stripe
#         }]
#
#
#     # Создаем сессию оплаты в Stripe
#     session = stripe.checkout.Session.create(**checkout_params)
#
#     return JsonResponse({'session_id': session.id})


def order_detail(request, order_id):
    """Отобразить детали заказа"""
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        "orders/order_detail.html",
        {"order": order, "stripe_public_key": settings.STRIPE_PUBLIC_KEY},
    )


def create_tax(request):
    """Создать налог в Stripe и сохранить его в базе данных"""
    try:
        # Создаем тариф налога в Stripe
        stripe_tax = stripe.TaxRate.create(
            display_name="VAT",
            percentage=20.0,  # 20% налог
            inclusive=True,  # Налог добавляется к сумме
        )

        # Сохраняем данные в базу данных
        tax = Tax.objects.create(
            tax_id=stripe_tax["id"],
            percentage=stripe_tax["percentage"],
            name=stripe_tax["display_name"],
        )

        return HttpResponse(
            f"Тариф налога успешно создан: {stripe_tax['id']} и сохранён в базе.",
            status=200,
        )

    except Exception as e:
        return HttpResponse(
            f"Произошла ошибка при создании тарифа налога: {e}", status=500
        )
