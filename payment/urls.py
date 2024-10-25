# Импортируем необходимые модули и функции для работы с маршрутизацией URL и представлениями.
from django.urls import path  # Функция для определения маршрутов URL.
from . import views, webhooks  # Импортируем представления и обработчики вебхуков из текущего приложения.

# Устанавливаем пространство имен для URL-шаблонов приложения 'payment'.
app_name = 'payment'

# Определяем список маршрутов URL для приложения 'payment'.
urlpatterns = [
    # URL для обработки платежа; обрабатывает путь 'process/'.
    path('process/', views.payment_process, name='process'),
    # URL для отображения страницы завершения платежа; обрабатывает путь 'completed/'.
    path('completed/', views.payment_completed, name='completed'),
    # URL для обработки отмены платежа; обрабатывает путь 'canceled/'.
    path('canceled/', views.payment_canceled, name='canceled'),
    # URL для обработки вебхуков от Stripe; обрабатывает путь 'webhook/'.
    path('webhook/', webhooks.stripe_webhook, name='webhook'),
]
