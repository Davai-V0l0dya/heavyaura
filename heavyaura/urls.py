"""
URL configuration for the heavyaura project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')

Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""

# Импортируем стандартные модули для администрирования и маршрутизации.
from django.contrib import admin
from django.urls import path, include  # Импортируем path и include для создания маршрутов.
from django.conf import settings  # Импортируем настройки проекта.
from django.conf.urls.static import static  # Импортируем функцию для обработки статических файлов.

# Определяем список маршрутов URL для всего проекта.
urlpatterns = [
    # URL маршрутов для админ-панели.
    path('admin/', admin.site.urls),
    
    # Включаем маршруты приложения 'cart' с пространством имен 'cart'.
    path('cart/', include('cart.urls', namespace='cart')),
    
    # Включаем маршруты приложения 'users' с пространством имен 'user'.
    path('user/', include('users.urls', namespace='user')),
    
    # Включаем маршруты приложения 'orders' с пространством имен 'orders'.
    path('orders/', include('orders.urls', namespace='orders')),
    
    # Включаем маршруты приложения 'payment' с пространством имен 'payment'.
    path('payment/', include('payment.urls', namespace='payment')),
    
    # Включаем маршруты основного приложения 'main' с пространством имен 'main'.
    path('', include('main.urls', namespace='main')),
]

# Если используется отладочный режим, добавляем поддержку статических файлов.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
