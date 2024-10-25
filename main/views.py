# Импортируем необходимые модули и классы из Django и приложения.
from django.shortcuts import render, get_object_or_404  # Функции для обработки запросов и получения объектов.
from django.core.paginator import Paginator  # Класс для постраничного отображения.
from .models import Product, Category  # Импортируем модели Product и Category.
from cart.forms import CartAddProductForm  # Импортируем форму для добавления продукта в корзину.

# Представление для отображения популярных продуктов (3 самых популярных).
def popular_list(request):
    # Получаем 3 доступных продукта.
    products = Product.objects.filter(available=True)[:3]
    # Отправляем список популярных продуктов в шаблон 'index.html'.
    return render(request,
                  'main/index/index.html',
                  {'products': products})

# Представление для отображения деталей конкретного продукта.
def product_detail(request, slug):
    # Получаем продукт по slug, если он доступен, иначе возвращаем 404.
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    # Создаем экземпляр формы для добавления продукта в корзину.
    cart_product_form = CartAddProductForm()
    # Отправляем продукт и форму в шаблон 'detail.html'.
    return render(request,
                  'main/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

# Представление для отображения списка продуктов (возможно, с фильтрацией по категории).
def product_list(request, category_slug=None):
    # Получаем номер страницы из GET-запроса, по умолчанию 1.
    page = request.GET.get('page', 1)
    category = None  # Инициализируем переменную категории как None.
    categories = Category.objects.all()  # Получаем все категории.
    
    # Получаем все доступные продукты.
    products = Product.objects.filter(available=True)
    
    # Создаем объект Paginator для постраничного отображения (по 10 продуктов на страницу).
    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))  # Получаем текущую страницу.

    if category_slug:
        # Если передан slug категории, получаем соответствующую категорию.
        category = get_object_or_404(Category,
                                     slug=category_slug)
        # Создаем объект Paginator для продуктов в данной категории.
        paginator = Paginator(products.filter(category=category), 10)
        current_page = paginator.page(int(page))  # Получаем текущую страницу для отфильтрованных продуктов.

    # Отправляем категорию, все категории, продукты на текущей странице и slug категории в шаблон 'list.html'.
    return render(request,
                  'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': current_page,
                   'slug_url': category_slug})
