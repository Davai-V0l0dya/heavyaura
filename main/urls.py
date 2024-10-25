# Импортируем функцию path для определения маршрутов URL и представления из текущего приложения.
from django.urls import path
from . import views  # Импортируем views из текущего модуля.

# Устанавливаем пространство имен для URL-шаблонов приложения 'main'.
app_name = 'main'

# Определяем список маршрутов URL для приложения 'main'.
urlpatterns = [
    # URL для отображения популярного списка продуктов; обрабатывает корневой путь.
    path('', views.popular_list, name='popular_list'),
    
    # URL для отображения списка всех продуктов; доступен по пути 'shop/'.
    path('shop/', views.product_list, name='product_list'),
    
    # URL для отображения детальной информации о продукте; ожидает slug продукта.
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # URL для отображения списка продуктов по категории; ожидает slug категории.
    path('shop/category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]
