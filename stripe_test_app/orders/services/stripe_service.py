import stripe
from django.conf import settings


class StripeService:
    @staticmethod
    def create_checkout_session(
        line_items, success_url, cancel_url, discount=None, tax=None
    ):
        """Создать Stripe Checkout Session"""
        checkout_params = {
            "payment_method_types": ["card"],
            "line_items": line_items,
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
        }

        # Добавляем скидку, если она есть
        if discount:
            checkout_params["discounts"] = [
                {
                    "coupon": discount.coupon_id,  # Используем coupon_id из Stripe
                }
            ]

        # # Добавляем налоговую ставку, если она есть
        # if tax:
        #     checkout_params['tax_rates'] = [tax.tax_id]  # Используем tax_id из Stripe

        # Создаем сессию оплаты в Stripe
        return stripe.checkout.Session.create(**checkout_params)
