# Импортируем Decimal для точных десятичных расчетов.
from decimal import Decimal
# Импортируем настройки проекта Django.
from django.conf import settings
# Импортируем модель Product из приложения main.
from main.models import Product

# Определяем класс для представления корзины покупок.
class Cart:
    # Метод инициализации, который принимает объект запроса.
    def init(self, request):
        # Сохраняем сессию из запроса.
        self.session = request.session
        # Получаем корзину из сессии, используя уникальный идентификатор корзины из настроек.
        cart = self.session.get(settings.CART_SESSION_ID)
        # Если корзина не найдена, создаем пустую корзину в сессии.
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        # Сохраняем корзину в атрибуте экземпляра.
        self.cart = cart
        
    # Метод для добавления товара в корзину.
    def add(self, product, quantity=1, override_quantity=False):
        # Преобразуем идентификатор продукта в строку для использования в корзине.
        product_id = str(product.id)
        
        # Если продукт еще не в корзине, инициализируем его с количеством и ценой.
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        
        # Если флаг overwrite_quantity установлен, заменяем количество товара.
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            # Увеличиваем количество товара в корзине.
            self.cart[product_id]['quantity'] += quantity
        
        # Сохраняем изменения в сессии.
        self.save()
        
    # Метод для применения изменений к сессии.
    def save(self):
        # Указываем, что сессия была изменена.
        self.session.modified = True
        
    # Метод для удаления товара из корзины.
    def remove(self, product):
        # Преобразуем идентификатор продукта в строку для доступа к корзине.
        product_id = str(product.id)
        # Если продукт есть в корзине, удаляем его.
        if product_id in self.cart:
            del self.cart[product_id]
            # Сохраняем изменения в сессии.
            self.save()
    
    # Метод для итерации по товарам в корзине.
    def iter(self):
        # Получаем идентификаторы продуктов из корзины.
        product_ids = self.cart.keys()
        # Извлекаем продукты из базы данных с использованием идентификаторов.
        products = Product.objects.filter(id__in=product_ids)
        # Копируем корзину для дальнейшей обработки.
        cart = self.cart.copy()
        
        # Обогащаем информацию о товарах, добавляя объект продукта в корзину.
        for product in products:
            cart[str(product.id)]['product'] = product
            
        # Обрабатываем каждый элемент в корзине.
        for item in cart.values():
            # Преобразуем цену из строки в Decimal для точных расчетов.
            item['price'] = Decimal(item['price'])
            # Вычисляем общую цену для каждого товара.
            item['total_price'] = item['price'] * item['quantity']
            # Используем yield для генерации элементов.
            yield item
            
    # Метод для получения общего количества товаров в корзине.
    def len(self):
        # Возвращаем сумму количеств всех товаров в корзине.
        return sum(item['quantity'] for item in self.cart.values())
    
    # Метод для очистки корзины.
    def clear(self):
        # Удаляем корзину из сессии.
        del self.session[settings.CART_SESSION_ID]
        
    # Метод для получения общей стоимости товаров в корзине.
    def get_total_price(self):
        # Вычисляем общую стоимость с учетом скидок.
        total = sum((Decimal(item['price']) - (Decimal(item['price']) \
            * Decimal(item['product'].discount / 100))) * item['quantity']
                for item in self.cart.values())
# Форматируем общую стоимость до двух знаков после запятой.
        return format(total, '.2f')
