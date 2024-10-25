import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from main.models import Product

# Обработка вебхука от Stripe
@csrf_exempt  # Декоратор, который отключает проверку CSRF для этого представления
def stripe_webhook(request):
    payload = request.body  # Получение тела запроса (payload) с данными от Stripe
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']  # Получение заголовка с подписью для проверки
    event = None  # Инициализация переменной для хранения события
    
    try:
        # Проверка подписи вебхука, чтобы убедиться в его подлинности
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET  # Секретный ключ для проверки подписи
        )
    except ValueError as e:
        # Возвращаем статус 400, если произошла ошибка при обработке (например, неверный JSON)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Возвращаем статус 400, если проверка подписи не удалась
        return HttpResponse(status=400)
    
    # Обработка события завершенной сессии покупки
    if event.type == 'checkout.session.completed':
        session = event.data.object  # Получаем объект сессии из события
        # Проверка, что это платежная сессия и статус оплаты — "оплачен"
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                # Получение заказа по id, который передан в качестве client_reference_id
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                # Если заказ не найден, возвращаем статус 404
                return HttpResponse(status=404)
                
            # Обновление состояния заказа: помечаем как оплаченный и сохраняем ID платежа
            order.paid = True
            order.stripe_id = session.payment_intent  # Сохраняем ID платежа от Stripe
            order.save()  # Сохраняем изменения в базе данных

    # Возвращаем статус 200, если обработка прошла успешно
    return HttpResponse(status=200)
