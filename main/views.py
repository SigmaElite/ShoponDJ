from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):   #c_slug=None т.к фильтр ниче не надо всё выводим,  щдесь будем вывод продукты
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:  #если в запросе у юзера есть параметр на фильтр то 
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'main/product/list.html', {'category': category, 'categories': categories, 'products': products})#с помощью 3(контекста) будем обр ко всему что запис в этом шаблоне


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)#в скобках указ какие продукты берём
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]#rel_p похожие продукты, берем продукты такой же категории как у продукта и доступность exclude указ чтоб не вывод нынеш продукт и вывод всего 4 доп продукта максимум
    cart_product_form = CartAddProductForm()

    return render(request, 'main/product/detail.html', {'product': product, 'related_products': related_products, 'cart_product_form': cart_product_form})
