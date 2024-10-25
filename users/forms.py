from django import forms
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UserChangeForm
from .models import User

# Форма для аутентификации пользователей
class UserLoginForm(AuthenticationForm):
    username = forms.CharField()  # Поле для ввода имени пользователя
    password = forms.CharField(widget=forms.PasswordInput)  # Поле для ввода пароля с маскировкой
    
    class Meta:
        model = User  # Указываем, что форма основана на модели User
        fields = ['username', 'password']  # Указываем, какие поля должны быть в форме
        
# Форма для регистрации новых пользователей
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User  # Указываем, что форма основана на модели User
        fields = (
            'first_name',  # Имя пользователя
            'last_name',   # Фамилия пользователя
            'username',    # Логин пользователя
            'email',       # Email адрес пользователя
            'password1',   # Первый ввод пароля
            'password2',   # Повторный ввод пароля
        )

# Поля для формы регистрации
        first_name = forms.CharField()  # Создаем поле для ввода имени
        last_name = forms.CharField()   # Создаем поле для ввода фамилии
        username = forms.CharField()     # Создаем поле для ввода логина
        email = forms.EmailField()       # Создаем поле для ввода email (используем EmailField для валидации)
        password1 = forms.CharField(widget=forms.PasswordInput)  # Поле для ввода первого пароля с маскировкой
        password2 = forms.CharField(widget=forms.PasswordInput)  # Поле для повторного ввода пароля с маскировкой
        
# Форма для изменения профиля пользователя
class ProfileForm(UserChangeForm):
    class Meta:
        model = User  # Указываем, что форма основана на модели User
        fields = (
            'image',      # Поле для загрузки изображения профиля
            'first_name', # Имя пользователя
            'last_name',  # Фамилия пользователя
            'username',   # Логин пользователя
            'email',      # Email адрес пользователя
        )
    
    # Поля для формы профиля
        image = forms.ImageField(required=False)  # Поле для загрузки изображения (необязательное)
        first_name = forms.CharField()            # Поле для ввода имени
        last_name = forms.CharField()             # Поле для ввода фамилии
        username = forms.CharField()              # Поле для ввода логина
        email = forms.EmailField()                # Поле для ввода email (используем EmailField для валидации)
