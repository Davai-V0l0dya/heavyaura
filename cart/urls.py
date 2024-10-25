# Импортируем функцию path для определения URL-шаблонов.
from django.urls import path
# Импортируем представления (views) из текущего приложения.
from . import views

# Устанавливаем пространство имен для URL-шаблонов приложения "cart".
app_name = 'cart'

# Определяем список URL-шаблонов для приложения корзины.
urlpatterns = [
    # URL для отображения деталей корзины. Здесь используется функция представления cart_detail.
    path('', views.cart_detail, name='cart_detail'),
    
    # URL для добавления продукта в корзину. Используется параметр product_id из URL.
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    
    # URL для удаления продукта из корзины. Используется параметр product_id из URL.
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
