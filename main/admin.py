# Импортируем необходимые модули из Django.
from django.contrib import admin  # Модуль для администрирования сайта.
from .models import Product, Category, ProductImage  # Импортируем модели, которые будут управляться через админ-панель.

# Регистрация модели Category в админ-панели.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Определяем поля, отображаемые в списке категорий.
    list_display = ['name', 'slug']
    # Автоматически заполняем поле slug на основе названия категории при создании/редактировании.
    prepopulated_fields = {'slug': ('name',)}

# Определяем Inline-класс для моделей изображений продуктов.
class ProductImageInline(admin.TabularInline):
    model = ProductImage  # Указываем модель, которая будет отображаться в виде инлайна.
    extra = 5  # Позволяем добавлять до 5 дополнительных изображений для каждого продукта.

# Регистрация модели Product в админ-панели.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Определяем поля, отображаемые в списке продуктов.
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated',
                    'discount']
    
    # Фильтры для быстрого поиска по полям.
    list_filter = ['available', 'created', 'updated']
    
    # Поля, которые могут редактироваться непосредственно из списка продуктов.
    list_editable = ['price', 'available', 'discount']
    
    # Автоматически заполняем поле slug на основе названия продукта при создании/редактировании.
    prepopulated_fields = {'slug': ('name',)}

    # Указываем, что ProductImageInline будет использоваться в форме редактирования продукта.
    inlines = [ProductImageInline]
