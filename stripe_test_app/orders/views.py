import stripe
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY



def buy_order(request, id):
    """получить Stripe Session Id для оплаты выбранного Item"""
    order = get_object_or_404(Order, id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            # TODO: remove hardcode
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'hardcode',
                },
                'unit_amount': int(order.total_cost * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'session_id': session.id})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    return render(
        request,
        'orders/order_detail.html',
        {'order': order, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    )


# class CheckoutView(View):
#     def get(self, request, *args, **kwargs):
#         order_id = kwargs.get('order_id')
#         try:
#             order = Order.objects.get(id=order_id)
#         except Order.DoesNotExist:
#             return HttpResponseBadRequest("Invalid order ID")
#
#         context = {
#             'order': order,
#             'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
#         }
#         return render(request, 'checkout.html', context)
#
#     def post(self, request, *args, **kwargs):
#         order_id = kwargs.get('order_id')
#         token = request.POST['stripeToken']
#         try:
#             order = Order.objects.get(id=order_id)
#         except Order.DoesNotExist:
#             return HttpResponseBadRequest("Invalid order ID")
#
#         try:
#             charge = stripe.Charge.create(
#                 amount=int(order.total_cost * 100),  # Convert to cents
#                 currency=order.items.first().item.currency.lower(),
#                 source=token,
#                 description=f'Charge for order {order.id}'
#             )
#
#             if charge.status == 'succeeded':
#                 order.stripe_payment_id = charge.id
#                 order.save()
#                 return redirect('payment_success')
#             else:
#                 return HttpResponseBadRequest("Payment failed")
#         except stripe.error.CardError as e:
#             body = e.json_body
#             err = body.get('error', {})
#             return HttpResponseBadRequest(f"{err.get('message')}")

