# Импортируем необходимые модули и классы для работы с моделями.
from django.db import models  # Модуль для создания моделей.
from main.models import Product  # Импортируем модель Product из приложения main.
from users.models import User  # Импортируем модель User из приложения users.
from django.conf import settings  # Импортируем настройки проекта.

# Определяем модель заказа.
class Order(models.Model):
    # Связь с пользователем (если есть); при удалении пользователя устанавливаем значение по умолчанию (None).
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,
                             blank=True, null=True, default=None)
    # Имя клиента.
    first_name = models.CharField(max_length=50)
    # Фамилия клиента.
    last_name = models.CharField(max_length=50)
    # Email клиента.
    email = models.EmailField()
    # Город доставки.
    city = models.CharField(max_length=100)
    # Адрес доставки.
    address = models.CharField(max_length=250)
    # Почтовый индекс.
    postal_code = models.CharField(max_length=20)
    # Дата и время создания заказа.
    created = models.DateTimeField(auto_now_add=True)
    # Дата и время последнего обновления заказа.
    updated = models.DateTimeField(auto_now=True)
    # Флаг, указывающий, оплачен ли заказ (по умолчанию False).
    paid = models.BooleanField(default=False)
    # Идентификатор Stripe для заказов, связанных с оплатой.
    stripe_id = models.CharField(max_length=250, blank=True)

    class Meta:
        # Указываем порядок сортировки по дате создания в порядке убывания.
        ordering = ['-created']
        # Индексируем поле 'created' для оптимизации запросов.
        indexes = [
            models.Index(fields=['-created']),
        ]

    # Метод для строкового представления заказа.
    def __str__(self):
        return f'Order {self.id}'

    # Метод для вычисления общей стоимости заказа на основе его элементов.
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # Метод для получения URL на страницу оплаты через Stripe.
    def get_stripe_url(self):
        if not self.stripe_id:
            return ''  # Возвращаем пустую строку, если stripe_id отсутствует.
        # Определяем путь для тестового или живого режима Stripe.
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


# Определяем модель элемента заказа.
class OrderItem(models.Model):
    # Связь с заказом; при удалении заказа, элементы заказа также будут удалены.
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    # Связь с продуктом; при удалении продукта элементы заказа также будут удалены.
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    # Цена продукта на момент заказа.
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    # Количество этого продукта в заказе.
    quantity = models.PositiveIntegerField(default=1)

    # Метод для строкового представления элемента заказа.
    def __str__(self):
        return str(self.id)

    # Метод для вычисления стоимости элемента заказа.
    def get_cost(self):
        return self.price * self.quantity
