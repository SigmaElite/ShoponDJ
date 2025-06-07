from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)#db index(прим к тому что часто юзаем при фильтр, добавл в нейм индекс) нужен для того чтоб созд полю индекс чтоб ускор работу бд
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)#тут указ как будут располог наши категории
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name 
    
    def get_absolute_url(self): #g_a_u получить страницу конкретного объекта из базы данных
        return reverse("main:product_list_by_category", args=[self.slug])#args аргументы
    


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)#FK с помощ ее засунули категори модель выше в этот стобец r_n как будет отобр в админке
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)#u_to куда будем загруж и указ в дату загруз, b=T указ что поле необязат т.е можем в амдинке его не заполн
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)#d_p числа после запят
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('name',)#отобр в админке сортировка по нейм

    def __str__(self):
        return self.name
    
    def get_absolute_url(self): #g_a_u получить страницу конкретного объекта из базы данных
        return reverse("main:product_detail", args=[self.id, self.slug])#reverse() — это способ в Django создать URL, args аргументы