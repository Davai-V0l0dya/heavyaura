# Импортируем функции и классы, необходимые для работы с представлениями и обработкой запросов.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart  # Импортируем класс Cart для работы с корзиной.
from .forms import CartAddProductForm  # Импортируем форму для добавления продуктов в корзину.

# Обрабатываем POST-запрос для добавления продукта в корзину.
@require_POST
def cart_add(request, product_id):
    # Создаём экземпляр корзины на основе текущего запроса.
    cart = Cart(request)
    
    # Получаем продукт по его идентификатору или возвращаем 404, если продукт не найден.
    product = get_object_or_404(Product, id=product_id)

    # Создаем форму с данными из POST-запроса.
    form = CartAddProductForm(request.POST)
    
    # Проверяем, что форма валидна.
    if form.is_valid():
        # Извлекаем очищенные данные из формы.
        cd = form.cleaned_data
        # Добавляем продукт в корзину с указанным количеством и флагом переопределения.
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    
    # Перенаправляем пользователя на страницу деталей корзины.
    return redirect('cart:cart_detail')


# Обрабатываем POST-запрос для удаления продукта из корзины.
@require_POST
def cart_remove(request, product_id):
    # Создаём экземпляр корзины на основе текущего запроса.
    cart = Cart(request)
    
    # Получаем продукт по его идентификатору или возвращаем 404, если продукт не найден.
    product = get_object_or_404(Product, id=product_id)
    
    # Удаляем продукт из корзины.
    cart.remove(product)
    
    # Перенаправляем пользователя на страницу деталей корзины.
    return redirect('cart:cart_detail')


# Отображаем страницу с деталями корзины.
def cart_detail(request):
    # Создаём экземпляр корзины на основе текущего запроса.
    cart = Cart(request)
    
    # Отображаем шаблон 'detail.html', передавая в контекст объект корзины.
    return render(request, 'cart/detail.html', {'cart': cart})
