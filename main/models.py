# Импортируем необходимые модули для работы с моделями и URL-адресами.
from django.db import models
from django.urls import reverse


class Category(models.Model):
    # Название категории - строка с максимальной длиной 20 символов, уникальная для каждой категории.
    name = models.CharField(max_length=20, unique=True)
    # Slug для категории - уникальная строка для формирования URL.
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        # Указываем порядок сортировки категорий по имени.
        ordering = ['name']
        # Индексируем поле name для быстрого поиска.
        indexes = [models.Index(fields=['name'])]
        # Задаем человекопонятные имена для модели.
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        # Возвращаем URL для отображения списка продуктов по категории.
        return reverse("main:product_list_by_category", args=[self.slug])

    def __str__(self):
        # Метод для строкового представления категории (возвращает имя).
        return self.name


class Product(models.Model):
    # Связь с категорией, с каскадным удалением связанных продуктов.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # Название продукта - строка с максимальной длиной 50 символов.
    name = models.CharField(max_length=50)
    # Slug для продукта, используемый в URL.
    slug = models.SlugField(max_length=50)
    # Поле для изображения продукта.
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    # Описание продукта - текстовое поле, не обязательное для заполнения.
    description = models.TextField(blank=True)
    # Цена продукта - десятичное поле.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Доступность продукта - булевое поле (по умолчанию True).
    available = models.BooleanField(default=True)
    # Дата создания продукта.
    created = models.DateTimeField(auto_now_add=True)
    # Дата последнего обновления продукта.
    updated = models.DateTimeField(auto_now=True)
    # Поле для указания скидки на продукт.
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)

    class Meta:
        # Указываем порядок сортировки продуктов по имени.
        ordering = ['name']
        # Индексируем поля для оптимизации запросов.
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        # Метод для строкового представления продукта (возвращает имя).
        return self.name

    def get_absolute_url(self):
        # Возвращаем URL для отображения деталей продукта.
        return reverse('main:product_detail', args=[self.slug])

    def sell_price(self):
        # Метод для вычисления цены со скидкой, если она есть.
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price


class ProductImage(models.Model):
    # Связь с продуктом, с каскадным удалением связанных изображений.
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    # Поле для изображения продукта.
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        # Метод для строкового представления изображения продукта.
        return f'{self.product.name} - {self.image.name}'
