# Импортируем необходимые функции и классы из Django и сторонних библиотек.
from django.shortcuts import render, redirect, get_object_or_404  # Функции для обработки запросов.
from django.urls import reverse  # Функция для получения URL по имени маршрута.
from decimal import Decimal  # Импортируем Decimal для работы с денежными значениями.
from orders.models import Order  # Импортируем модель Order из приложения orders.
from django.conf import settings  # Импортируем настройки проекта.
import stripe  # Импортируем библиотеку Stripe для обработки платежей.

# Устанавливаем секретный ключ и версию API для Stripe.
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

# Представление для обработки платежа.
def payment_process(request):
    # Извлекаем ID заказа из сессии; если нет - возвращаем 404.
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    
    # Обрабатываем POST-запрос, когда пользователь инициирует платеж.
    if request.method == 'POST':
        # Определяем URL-адреса для успешного завершения и отмены платежа.
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Создаем данные для сессии платежа.
        session_data = {
            'mode': 'payment',  # Режим платежа.
            'client_reference_id': order.id,  # Ссылаемся на ID заказа для идентификации.
            'success_url': success_url,  # URL для успешного завершения платежа.
            'cancel_url': cancel_url,  # URL для отмены платежа.
            'line_items': []  # Список товаров в заказе.
        }
        
        # Заполняем список line_items с товарами из заказа.
        for item in order.items.all():  # Перебираем все элементы заказа.
            discounted_price = item.product.sell_price()  # Получаем цену со скидкой продукта.
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(discounted_price * Decimal('100')),  # Указываем сумму в центах.
                    'currency': 'usd',  # Указываем валюту.
                    'product_data': {
                        'name': item.product.name,  # Название продукта.
                    },
                },
                'quantity': item.quantity,  # Указываем количество.
            })
        
        # Создаем сессию платежа в Stripe с указанными данными.
        session = stripe.checkout.Session.create(**session_data)
        
        # Перенаправляем пользователя на страницу оплаты Stripe.
        return redirect(session.url, code=303)
    
    # Если запрос не POST, рендерим страницу процессинга платежа.
    else:
        return render(request, 'payment/process.html', locals())

# Представление для отображения страницы завершения платежа.
def payment_completed(request):
    return render(request, 'payment/completed.html')

# Представление для отображения страницы отмены платежа.
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
