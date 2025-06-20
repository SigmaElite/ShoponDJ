from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Обработка категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Обработка поиска - ЭТО БЫЛО ПРОПУЩЕНО!
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
    }
    
    return render(request, 'main/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'main/product/detail.html', {'product': product})

def live_search(request):
    """API для живого поиска товаров"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({
            'products': [],
            'count': 0,
            'query': query
        })
    
    # Поиск товаров
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query),
        available=True
    )[:8]
    
    # Формируем данные для JSON
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'image': product.image.url if product.image else '/static/img/no-image.png',
            'url': product.get_absolute_url(),
            'category': product.category.name if product.category else '',
        })
    
    total_count = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query),
        available=True
    ).count()
    
    return JsonResponse({
        'products': products_data,
        'count': len(products_data),
        'query': query,
        'total_found': total_count
    })