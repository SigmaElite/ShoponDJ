from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}#prep_f поля которые заполн автомат

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']  
    list_filter = ['available', 'created', 'updated', 'category']#фильтрация по характеристикам
    list_editable = ['price', 'available']#редакт опред поля прямо со стр списка объектов в админке т.е не заход на сам товар
    prepopulated_fields = {'slug': ('name',)}