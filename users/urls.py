from django.urls import path  # Импортируем функцию path для определения маршрутов
from . import views  # Импортируем представления из текущего приложения

app_name = 'users'  # Устанавливаем пространство имен для маршрутов в приложении пользователей

# Определение URL-шаблонов для приложения пользователей
urlpatterns = [
    path('login/', views.login, name='login'),  # Маршрут для страницы входа; вызывает представление login
    path('registration/', views.registration, name='registration'),  # Маршрут для страницы регистрации; вызывает представление registration
    path('profile/', views.profile, name='profile'),  # Маршрут для страницы профиля пользователя; вызывает представление profile
    path('logout/', views.logout, name='logout'),  # Маршрут для выхода из аккаунта; вызывает представление logout
]
