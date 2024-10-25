# Импортируем необходимые модули из Django.
from django.contrib import admin  # Модуль для административного интерфейса.
from .models import Order, OrderItem  # Импортируем модели заказа и элемента заказа.
from django.utils.safestring import mark_safe  # Функция для безопасного вывода HTML-кода.

# Определяем класс инлайна для элементов заказа в админ-панели.
class OrderItemInline(admin.TabularInline):
    model = OrderItem  # Указываем модель элемента заказа.
    raw_id_fields = ['product']  # Отображаем поле 'product' как raw ID поле для выбора продукта.

# Функция для отображения ссылки на оплату через Stripe.
def order_stripe_payment(obj):
    url = obj.get_stripe_url()  # Получаем URL для оплаты через Stripe.
    if obj.stripe_id:  # Проверяем, установлен ли `stripe_id`.
        # Генерируем HTML-ссылку на оплату с открытием в новой вкладке.
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)  # Возвращаем безопасный HTML-код для вывода.
    return ''  # Если нет `stripe_id`, возвращаем пустую строку.

# Устанавливаем описание для нового поля в админке.
order_stripe_payment.short_description = 'Stripe payment'

# Регистрация модели Order в админ-панели.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Определяем поля, отображаемые в списке заказов в админке.
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city', 'paid',
        order_stripe_payment, 'created', 'updated'
    ]
    
    # Определяем фильтры для удобного поиска по полям.
    list_filter = ['paid', 'created', 'updated']
    
    # Указываем, что элементы заказа будут отображаться как инлайн-элементы.
    inlines = [OrderItemInline]
