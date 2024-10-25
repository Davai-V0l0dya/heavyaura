# Импортируем функцию path для определения маршрутов URL и представления из текущего приложения.
from django.urls import path
from . import views  # Импортируем views из текущего модуля.

# Устанавливаем пространство имен для URL-шаблонов приложения 'orders'.
app_name = 'orders'

# Определяем список маршрутов URL для приложения 'orders'.
urlpatterns = [
    # URL для создания нового заказа; обрабатывает путь 'create/'.
    path('create/', views.order_create, name='order_create'),
]
