# Импортируем необходимые модули и классы из Django и приложения.
from django.shortcuts import render, redirect  # Функции для обработки запросов.
from django.urls import reverse  # Функция для получения URL по названию маршрута.
from .models import OrderItem  # Импортируем модель OrderItem.
from .forms import OrderCreateForm  # Импортируем форму для создания заказа.
from cart.cart import Cart  # Импортируем класс Cart для работы с корзиной.

# Представление для создания заказа.
def order_create(request):
    cart = Cart(request)  # Инициализируем корзину на основе текущего запроса.
    
    # Обрабатываем POST-запрос, когда форма отправлена.
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)  # Создаем объект формы с POST-данными.
        
        # Проверяем, валидна ли форма.
        if form.is_valid():  
            order = form.save()  # Сохраняем заказ и получаем объект заказа.
            
            # Перебираем элементы в корзине и создаем для каждого элемента записи OrderItem.
            for item in cart:
                discounted_price = item['product'].sell_price()  # Получаем цену со скидкой продукта.
                OrderItem.objects.create(order=order,  # Создаем элемент заказа.
                                         product=item['product'],
                                         price=discounted_price,
                                         quantity=item['quantity'])
            cart.clear()  # Очищаем корзину после создания заказа.
            request.session['order_id'] = order.id  # Сохраняем ID заказа в сессии.
            
            # Перенаправляем пользователя на страницу обработки платежа.
            return redirect(reverse('payment:process'))
    
    # Если запрос не POST, создаем пустую форму.
    else:
        form = OrderCreateForm(request=request)
    
    # Отправляем текущую корзину и форму в шаблон для отображения.
    return render(request, 
                  'orders/order/create.html',
                  {'cart': cart,
                   'form': form})
