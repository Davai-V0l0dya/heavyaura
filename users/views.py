from django.shortcuts import render, redirect  # Импортируем функции для работы с представлениями
from django.contrib import auth, messages  # Импортируем аутентификацию и систему сообщений
from django.urls import reverse  # Импортируем функцию для обратного разрешения URL
from django.http import HttpResponseRedirect  # Импортируем класс для перенаправления HTTP
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm  # Импортируем формы для входа, регистрации и профиля пользователя
from django.contrib.auth.decorators import login_required  # Импортируем декоратор для защиты представлений от неавторизованных пользователей
from django.db.models import Prefetch  # Импортируем Prefetch для оптимизации запросов к базе данных
from orders.models import Order, OrderItem  # Импортируем модели заказов и товаров в заказе

# Представление для входа пользователя
def login(request):
    if request.method == 'POST':  # Если запрос - POST, значит, пользователь отправил форму
        form = UserLoginForm(data=request.POST)  # Создаем форму с данными POST
        if form.is_valid():  # Проверяем, является ли форма валидной
            username = request.POST['username']  # Получаем имя пользователя из данных POST
            password = request.POST['password']  # Получаем пароль из данных POST
            user = auth.authenticate(username=username, password=password)  # Проверяем учётные данные
            if user:  # Если аутентификация успешна
                auth.login(request, user)  # Входим в систему с указанным пользователем
                return HttpResponseRedirect(reverse('main:product_list'))  # Перенаправляем на страницу со списком продуктов
    else:
        form = UserLoginForm()  # Если запрос не POST, создаем пустую форму
    return render(request, 'users/login.html', {'form': form})  # Отображаем страницу входа с формой

# Представление для регистрации нового пользователя
def registration(request):
    if request.method == 'POST':  # Если запрос - POST, значит, пользователь отправил форму
        form = UserRegistrationForm(data=request.POST)  # Создаем форму с данными POST
        if form.is_valid():  # Проверяем, является ли форма валидной
            form.save()  # Сохраняем нового пользователя
            user = form.instance  # Получаем нового пользователя
            auth.login(request, user)  # Входим в систему с этим пользователем
            messages.success(request, f'{user.username}, Successful Registration')  # Отправляем сообщение об успехе
            return HttpResponseRedirect(reverse('user:login'))  # Перенаправляем на страницу входа
    else:
        form = UserRegistrationForm()  # Если запрос не POST, создаем пустую форму
    return render(request, 'users/registration.html')  # Отображаем страницу регистрации

# Защищенное представление для отображения и редактирования профиля пользователя
@login_required
def profile(request):
    if request.method == 'POST':  # Если запрос - POST, значит, пользователь отправил форму
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)  # Создаем форму с данными пользователя
        if form.is_valid():  # Проверяем, является ли форма валидной
            form.save()  # Сохраняем изменения профиля
            messages.success(request, 'Profile was changed')  # Отправляем сообщение об успехе
            return HttpResponseRedirect(reverse('user:profile'))  # Перенаправляем на страницу профиля
    else:
        form = ProfileForm(instance=request.user)  # Если запрос не POST, создаем форму с текущими данными пользователя

    # Получаем заказы пользователя с предварительной выборкой связанных товаров
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product'),
        )
    ).order_by('-id')  # Упорядочиваем заказы по убыванию
    return render(request, 'users/profile.html',
                  {'form': form,  # Передаем форму профиля
                   'orders': orders})  # Передаем заказы пользователя

# Представление для выхода пользователя из системы
def logout(request):
    auth.logout(request)  # Выполняем выход из системы
    return redirect(reverse('main:product_list'))  # Перенаправляем на страницу со списком продуктов
