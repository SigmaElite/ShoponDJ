from django.conf import settings
from main.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)#получ сессию юзера(его корзину)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}#если корзины нет то задаём её пустой кортеж и оставл так
        self.cart = cart#тут корзина становится с теми товарами которые он добавл

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart: #проверяем есть ли продукт в корзине
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:#если меняет колво с 1 на 10 и т.п, если он перезапис колво товара в корзине самостоятельно
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True   #тут указ что поменяли сессию

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]#удаляем продукт по его айди
            self.save()
    
    def __iter__(self):#  итерация проход по всем товарам в корзине и позвол с ними работать
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)#Берём из БД только те товары, которые есть в корзине
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product#к каждой записи в корзине добавл реал объект товара из БД

        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item #дать один товар(item) из корзины и подождать, пока потребуется следующий
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())#возвращ количество по которому прошлись и суммируем его

    def get_total_price(self):  #итоговая стомисть всех товаров в корзине
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
