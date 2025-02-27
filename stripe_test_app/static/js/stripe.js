// Получаем данные для Payment Intent
fetch(`/intent_buy/${itemId}/`)
    .then(response => response.json())
    .then(data => {
        const stripe = Stripe(data.publishableKey);
        const elements = stripe.elements();

        // Создаем отдельные элементы для номера карты, срока действия и CVC
        const cardNumber = elements.create('cardNumber', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#32325d',
                    '::placeholder': {
                        color: '#aab7c4',
                    },
                },
                invalid: {
                    color: '#fa755a',
                },
            },
        });
        cardNumber.mount('#card-number');

        const cardExpiry = elements.create('cardExpiry', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#32325d',
                    '::placeholder': {
                        color: '#aab7c4',
                    },
                },
                invalid: {
                    color: '#fa755a',
                },
            },
        });
        cardExpiry.mount('#card-expiry');

        const cardCvc = elements.create('cardCvc', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#32325d',
                    '::placeholder': {
                        color: '#aab7c4',
                    },
                },
                invalid: {
                    color: '#fa755a',
                },
            },
        });
        cardCvc.mount('#card-cvc');

        const form = document.getElementById('payment-form');
        const errorMessage = document.getElementById('error-message');

        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Отключаем кнопку, чтобы предотвратить повторные нажатия
            document.getElementById('submit-button').disabled = true;

            // Создаем платежный метод с использованием отдельных элементов
            const { error, paymentMethod } = await stripe.createPaymentMethod({
                type: 'card',
                card: cardNumber,
                billing_details: {
                    // Здесь можно добавить дополнительные данные, например, имя и адрес
                },
            });

            if (error) {
                // Показываем ошибку
                errorMessage.textContent = error.message;
                // Включаем кнопку снова
                document.getElementById('submit-button').disabled = false;
            } else {
                // Подтверждаем платеж с использованием Payment Intent
                const { error: confirmError, paymentIntent } = await stripe.confirmCardPayment(
                    data.clientSecret, {
                        payment_method: paymentMethod.id,
                    }
                );

                if (confirmError) {
                    // Показываем ошибку
                    errorMessage.textContent = confirmError.message;
                    // Включаем кнопку снова
                    document.getElementById('submit-button').disabled = false;
                } else {
                    // Перенаправляем на страницу успеха
                    window.location.href = '/success/';
                }
            }
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });