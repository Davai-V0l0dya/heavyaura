# Импортируем модули Django для работы с формами и моделью заказа.
from django import forms
from .models import Order  # Импортируем модель Order для создания формы.

# Определяем форму для создания заказа, наследуя от ModelForm.
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order  # Указываем, что данная форма основана на модели Order.
        # Определяем поля, которые будут включены в форму.
        fields = ['user', 'first_name', 'last_name', 'email',
                  'address', 'postal_code', 'city']

    # Метод инициализации формы.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Извлекаем request из аргументов.
        super().__init__(*args, **kwargs)  # Вызываем родительский метод инициализации.
        # Если пользователь аутентифицирован, предустанавливаем его данные в форму.
        if self.request.user.is_authenticated:
            self.initial['first_name'] = self.request.user.first_name
            self.initial['last_name'] = self.request.user.last_name
            self.initial['email'] = self.request.user.email

    # Переопределяем метод сохранения формы.
    def save(self, commit=True):
        # Создаем объект заказа, но не сохраняем его сразу.
        order = super().save(commit=False)
        order.user = self.request.user  # Привязываем заказ к текущему пользователю.
        if commit:  # Если коммитить, сохраняем объект в базе данных.
            order.save()
        return order  # Возвращаем объект заказа.
